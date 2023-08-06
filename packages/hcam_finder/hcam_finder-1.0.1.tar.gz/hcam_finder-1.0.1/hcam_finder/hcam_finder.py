# -*- coding: utf-8 -*-
from __future__ import print_function, absolute_import, unicode_literals, division
import tempfile
import threading
import os
from functools import partial
import six
from os.path import expanduser
import json

import numpy as np
from ginga.util import catalog, dp, wcs
from ginga.canvas.types.all import (Path, Circle,
                                    CompoundObject)
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates.name_resolve import NameResolveError

import hcam_widgets.widgets as w
from hcam_widgets.compo.utils import (InjectionArm, PickoffArm, INJECTOR_THETA, PARK_POSITION)
from hcam_widgets.tkutils import get_root

from .finding_chart import make_finder
from .shapes import (CCDWin, CompoPatrolArc, CompoFreeRegion)

has_astroquery = True
try:
    from .skyview import SkyviewImageServer
except ImportError:
    has_astroquery = False

if not six.PY3:
    import Tkinter as tk
    import tkFileDialog as filedialog
else:
    import tkinter as tk
    from tkinter import filedialog

# Image Archives
image_archives = [('ESO', 'ESO DSS', catalog.ImageServer,
                  "http://archive.eso.org/dss/dss?ra=%(ra)s&dec=%(dec)s&mime-type=application/x-fits&x=%(width)s&y=%(height)s",
                   "ESO DSS archive"),
                  ('ESO', 'ESO DSS2 Red', catalog.ImageServer,
                   "http://archive.eso.org/dss/dss?ra=%(ra)s&dec=%(dec)s&mime-type=application/x-fits&x=%(width)s&y=%(height)s&Sky-Survey=DSS2-red",
                   "ESO DSS2 Red"),
                  ('ESO', 'ESO DSS2 Blue', catalog.ImageServer,
                   "http://archive.eso.org/dss/dss?Sky-Survey=DSS2-blue&ra=%(ra)s&dec=%(dec)s&mime-type=application/x-fits&x=%(width)s&y=%(height)s",
                   "ESO DSS2 Blue"),
                  ('ESO', 'ESO DSS2 IR', catalog.ImageServer,
                   "http://archive.eso.org/dss/dss?Sky-Survey=DSS2-infrared&ra=%(ra)s&dec=%(dec)s&mime-type=application/x-fits&x=%(width)s&y=%(height)s",
                   "ESO DSS2 IR")]

if has_astroquery:
    image_archives.extend([
                    ('SDSS', 'SDSS u', SkyviewImageServer,
                     "SDSSu",
                     "Skyview SDSS g"),
                    ('SDSS', 'SDSS g', SkyviewImageServer,
                     "SDSSg",
                     "Skyview SDSS g"),
                    ('SDSS', 'SDSS r', SkyviewImageServer,
                     "SDSSr",
                     "Skyview SDSS r"),
                    ('SDSS', 'SDSS i', SkyviewImageServer,
                     "SDSSi",
                     "Skyview SDSS i"),
                    ('SDSS', 'SDSS z', SkyviewImageServer,
                     "SDSSz",
                     "Skyview SDSS z"),
                    ('2MASS', '2MASS J', SkyviewImageServer,
                     "2MASS-J",
                     "Skyview 2MASS J")
                    ])


@u.quantity_input(px_val=u.pix)
@u.quantity_input(px_scale=u.arcsec/u.pix)
def _px_deg(px_val, px_scale):
    """
    convert from pixels to degrees
    """
    return px_val.to(
        u.deg,
        equivalencies=u.pixel_scale(px_scale)
    ).value


@u.quantity_input(deg_val=u.deg)
@u.quantity_input(px_scale=u.arcsec/u.pix)
def _deg_px(deg_val, px_scale):
    """
    convert from degrees/arcmins etc to pixels
    """
    return deg_val.to(
        u.pix,
        equivalencies=u.pixel_scale(px_scale)
    ).value


class TelChooser(tk.Menu):
    """
    Provides a menu to choose the telescope.

    The telescope setting affects the signal/noise calculations
    and routines for pulling RA/Dec etc from the TCS.
    """
    def __init__(self, master, command, *args):
        """
        Parameters
        ----------
        master : tk.Widget
            the containing widget, .e.g toolbar menu
        """
        tk.Menu.__init__(self, master, tearoff=0)
        g = get_root(self).globals

        self.val = tk.StringVar()
        tel = g.cpars.get('telins_name', list(g.TINS)[0])
        self.val.set(tel)
        self.val.trace('w', self._change)
        for tel_name in g.TINS.keys():
            self.add_radiobutton(label=tel_name, value=tel_name, variable=self.val)
        self.args = args
        self.root = master
        self.command = command

    def _change(self, *args):
        g = get_root(self).globals
        g.cpars['telins_name'] = self.val.get()
        g.count.update()
        self.command()


class FovSetter(tk.LabelFrame):

    def __init__(self, master, fitsimage, logger):
        """
        fitsimage is reverence to ImageViewCanvas
        """
        tk.LabelFrame.__init__(self, master, pady=2, text='Object')

        self.fitsimage = fitsimage

        g = get_root(self).globals
        self.set_telins(g)

        row = 0
        column = 0
        tk.Label(self, text='Object Name').grid(row=row, column=column, sticky=tk.W)

        row += 1
        tk.Label(self, text='or Coords').grid(row=row, column=column, sticky=tk.W)

        row += 2
        tk.Label(self, text='Tel. RA').grid(row=row, column=column, sticky=tk.W)

        row += 1
        tk.Label(self, text='Tel. Dec').grid(row=row, column=column, sticky=tk.W)

        row += 1
        tk.Label(self, text='Tel. PA').grid(row=row, column=column, sticky=tk.W)

        # spacer
        column += 1
        tk.Label(self, text=' ').grid(row=0, column=column)

        row = 0
        column += 1
        self.targName = w.TextEntry(self, 22)
        self.targName.bind('<Return>', lambda event: self.query_simbad())
        self.targName.grid(row=row, column=column, sticky=tk.W)

        row += 1
        self.targCoords = w.TextEntry(self, 22)
        self.targCoords.grid(row=row, column=column, sticky=tk.W)

        row += 1
        surveyList = [archive[1] for archive in image_archives]
        self.surveySelect = w.Choice(self, surveyList, width=20)
        self.surveySelect.grid(row=row, column=column, sticky=tk.W)

        row += 1
        self.ra = w.Sexagesimal(self, callback=self.update_pointing_cb, unit='hms', width=10)
        self.ra.grid(row=row, column=column, sticky=tk.W)

        row += 1
        self.dec = w.Sexagesimal(self, callback=self.update_pointing_cb, unit='dms', width=10)
        self.dec.grid(row=row, column=column, sticky=tk.W)

        row += 1
        self.pa = w.PABox(self, 0.0, 0.0, 359.99, self.update_rotation_cb,
                          False, True, width=6, nplaces=2)
        self.pa.grid(row=row, column=column, sticky=tk.W)

        column += 1
        row = 0
        self.query = tk.Button(self, width=14, fg='black', bg=g.COL['main'],
                               text='Query Simbad', command=self.query_simbad)
        self.query.grid(row=row, column=column, sticky=tk.W)

        row += 2
        self.launchButton = tk.Button(self, width=14, fg='black',
                                      text='Load Image', bg=g.COL['main'],
                                      command=self.set_and_load)
        self.launchButton.grid(row=row, column=column, sticky=tk.W)

        self.imfilepath = None
        self.logger = logger

        # add callbacks to fits viewer for dragging FOV around
        self.fitsimage.canvas.add_callback('cursor-down', self.click_cb)
        self.fitsimage.canvas.add_callback('cursor-move', self.click_drag_cb)
        self.fitsimage.canvas.add_callback('cursor-up', self.click_release_cb)
        self.currently_moving_fov = False
        self.currently_rotating_fov = False

        # Add our image servers
        self.bank = catalog.ServerBank(self.logger)
        for (longname, shortname, klass, url, description) in image_archives:
            obj = klass(self.logger, longname, shortname, url, description)
            self.bank.addImageServer(obj)
        self.tmpdir = tempfile.mkdtemp()

        # current dither index
        self.dither_index = 0

        # catalog servers
        """
        for longname in conesearch.list_catalogs():
            shortname = longname
            url = ""    # astropy conesearch doesn't need URL
            description = longname
            obj = catalog.AstroPyCatalogServer(logger, longname, shortname,
                                               url, description)
            self.bank.addCatalogServer(obj)
        """

        # canvas that we will draw on
        self.canvas = fitsimage.canvas

        root = get_root(self)
        menubar = tk.Menu(root)
        fileMenu = tk.Menu(menubar, tearoff=0)
        fileMenu.add_command(label='Finding Chart', command=self.publish)
        fileMenu.add_command(label='Inst. Setup File', command=self.saveconf)
        # telescope chooser
        telChooser_cmd = partial(self.set_telins, g=g)
        telChooser = TelChooser(menubar, telChooser_cmd)

        menubar.add_cascade(label='Telescope', menu=telChooser)
        menubar.add_cascade(label='Save', menu=fileMenu)
        root.config(menu=menubar)

    def targetMarker(self):
        g = get_root(self).globals
        coo = SkyCoord(self.targCoords.value(),
                       unit=(u.hour, u.deg))
        image = self.fitsimage.get_image()
        x, y = image.radectopix(coo.ra.deg, coo.dec.deg)
        size = 10 if g.cpars['telins_name'] == 'WHT' else 3
        circ = Circle(x, y, size, fill=True,
                      color='red', fillalpha=0.3)
        self.canvas.deleteObjectByTag('Target')
        self.canvas.add(circ, tag='Target', redraw=True)

    def window_string(self):
        g = get_root(self).globals
        wframe = g.ipars.wframe
        if g.ipars.isFF():
            winlist = []
        if g.ipars.isDrift():
            winlist = [
                'xsl: {}, xsr: {}, ys: {}, nx: {}, ny: {}'.format(xsl, xsr, ys, nx, ny)
                for (xsl, xsr, ys, nx, ny) in wframe
            ]
        else:
            winlist = [
                'xsll: {}, xslr: {}, xsul: {}, xsur: {}, ys: {}, nx: {}, ny: {}'.format(
                    xsll, xslr, xsul, xsur, ys, nx, ny
                ) for (xsll, xsul, xslr, xsur, ys, nx, ny) in wframe
            ]
        return '\n'.join(winlist)

    def saveconf(self):
        fname = filedialog.asksaveasfilename(
            initialdir=expanduser("~"),
            defaultextension='.json',
            filetypes=[('config files', '.json')],
            title='Name of setup file')
        if not fname:
            print('Aborted save to disk')
            return False

        g = get_root(self).globals
        data = dict()
        data['appdata'] = g.ipars.dumpJSON()

        # add user info that we should know of
        # includes target, user and proposal
        user = dict()
        user['target'] = self.targName.value()
        data['user'] = user

        # target info
        target = dict()
        target['target'] = self.targName.value()
        targ_coord = SkyCoord(self.targCoords.value(), unit=(u.hour, u.deg))
        target['TARG_RA'] = targ_coord.ra.to_string(sep=':', unit=u.hour, pad=True, precision=2)
        target['TARG_DEC'] = targ_coord.dec.to_string(sep=':', precision=1, unit=u.deg,
                                                      alwayssign=False, pad=True)
        target['RA'] = self.ra._value.to_string(sep=':', unit=u.hour, pad=True, precision=2)
        target['DEC'] = self.dec._value.to_string(sep=':', precision=1, pad=True, unit=u.deg, alwayssign=False)
        target['PA'] = self.pa.value()
        data['target'] = target

        # write file
        with open(fname, 'w') as of:
            of.write(json.dumps(data, sort_keys=True, indent=4,
                                separators=(',', ': ')))
        print('Saved setup to ' + fname)
        return True

    def publish(self):
        g = get_root(self).globals
        arr = self.fitsimage.get_image_as_array()
        make_finder(self.logger, arr, self.targName.value(), g.cpars['telins_name'],
                    self.ra.as_string(), self.dec.as_string(), self.pa.value(),
                    self.window_string())

    @property
    def servername(self):
        return self.surveySelect.value()

    def click_cb(self, *args):
        canvas, event, x, y = args
        try:
            obj = self.canvas.get_object_by_tag('ccd_overlay')
            self.currently_moving_fov = obj.contains(x, y)
            if self.currently_moving_fov:
                self.ref_pos_x = x
                self.ref_pos_y = y
            else:
                mainCCD = None
                for thing in obj.objects:
                    if thing.name == 'mainCCD':
                        mainCCD = thing
                points = np.array(mainCCD.points)
                ref = np.array((x, y))
                dists = np.sum(np.sqrt((points-ref)**2), axis=1)
                if np.any(dists < 20):
                    self.currently_rotating_fov = True
                    self.ref_pa = np.degrees(
                        np.arctan2(y - self.ctr_y, x - self.ctr_x))
        except Exception as err:
            errmsg = "failed to draw CCD: {}".format(str(err))
            self.logger.warn(errmsg)

    def click_drag_cb(self, *args):
        canvas, event, x, y = args
        image = self.fitsimage.get_image()
        if self.currently_moving_fov and image is not None:
            xoff = x - self.ref_pos_x
            yoff = y - self.ref_pos_y
            new_ra, new_dec = image.pixtoradec(self.ctr_x + xoff,
                                               self.ctr_y + yoff)
            self.ref_pos_x = x
            self.ref_pos_y = y
            # update ra, dec boxes; triggers redraw callback
            self.ra.set(new_ra)
            self.dec.set(new_dec)
        elif self.currently_rotating_fov and image is not None:
            pa = np.degrees(np.arctan2(y - self.ctr_y, x - self.ctr_x))
            delta_pa = pa - self.ref_pa
            if not self.EofN:
                delta_pa *= -1
            self.pa.set(self.pa.value() + delta_pa)
            self.ref_pa = pa

    def click_release_cb(self, *args):
        canvas, event, x, y = args
        self.currently_moving_fov = False
        self.currently_rotating_fov = False

    def set_telins(self, g):
        telins = g.cpars['telins_name']
        self.px_scale = g.cpars[telins]['px_scale'] * u.arcsec/u.pix
        self.nxtot = g.cpars[telins]['nxtot'] * u.pix
        self.nytot = g.cpars[telins]['nytot'] * u.pix
        self.fov_x = _px_deg(self.nxtot, self.px_scale)
        self.fov_y = _px_deg(self.nytot, self.px_scale)

        # rotator centre position in pixels
        self.rotcen_x = g.cpars[telins]['rotcen_x'] * u.pix
        self.rotcen_y = g.cpars[telins]['rotcen_y'] * u.pix
        # is image flipped E-W?
        self.flipEW = g.cpars[telins]['flipEW']
        self.fitsimage.t_['flip_x'] = self.flipEW
        # does increasing PA rotate towards east from north?
        self.EofN = g.cpars[telins]['EofN']
        # rotator position in degrees when chip runs N-S
        self.paOff = g.cpars[telins]['paOff']
        if hasattr(self, 'fitsimage'):
            self.draw_ccd()

    @property
    def ctr_ra_deg(self):
        return self.ra.value()

    @property
    def ctr_dec_deg(self):
        return self.dec.value()

    def query_simbad(self):
        g = get_root(self).globals
        try:
            coo = SkyCoord.from_name(self.targName.value())
        except NameResolveError:
            self.targName.config(bg='red')
            self.logger.warn(msg='Could not resolve target')
            return
        self.targName.config(bg=g.COL['main'])
        self.targCoords.set(coo.to_string(style='hmsdms', sep=':'))

    def update_pointing_cb(self, *args):
        image = self.fitsimage.get_image()
        if image is None:
            return
        try:
            objs = [self.canvas.get_object_by_tag('ccd_overlay'),
                    self.canvas.get_object_by_tag('compo_overlay')]

            ctr_x, ctr_y = image.radectopix(self.ctr_ra_deg, self.ctr_dec_deg)
            self.ctr_x, self.ctr_y = ctr_x, ctr_y
            old_x, old_y = image.radectopix(self.ra_as_drawn, self.dec_as_drawn)
            for obj in objs:
                if obj is not None:
                    obj.move_delta(ctr_x - old_x, ctr_y - old_y)
            self.canvas.update_canvas()
            self.ra_as_drawn = self.ctr_ra_deg
            self.dec_as_drawn = self.ctr_dec_deg
        except Exception:
            self.draw_ccd(*args)

    def update_rotation_cb(self, *args):
        image = self.fitsimage.get_image()
        if image is None:
            return
        try:
            objs = [self.canvas.get_object_by_tag('ccd_overlay'),
                    self.canvas.get_object_by_tag('compo_overlay')]
            pa = self.pa.value() - self.paOff
            if not self.EofN:
                pa *= -1
            for obj in objs:
                if obj is not None:
                    obj.rotate(pa - self.pa_as_drawn, self.ctr_x, self.ctr_y)
            self.canvas.update_canvas()
            self.pa_as_drawn = pa
        except Exception:
            self.draw_ccd(*args)

    def _step_ccd(self):
        """
        Move CCD to next nod position
        """
        g = get_root(self).globals
        try:
            np = g.ipars.nodPattern
            if not np:
                raise ValueError('no nod pattern defined')
            nd = len(np['ra'])
            di = self.dither_index % nd
            raoff = np['ra'][di]
            decoff = np['dec'][di]
            self.dither_index += 1
        except Exception as err:
            self.logger.warn('could not get dither position {}: {}'.format(di, str(err)))
            return

        self.logger.info('moving CCD to dither position {:d} ({} {})'.format(
            di, raoff, decoff
        ))

        # get new dither cen
        ra, dec = wcs.add_offset_radec(
            self.ctr_ra_deg, self.ctr_dec_deg,
            raoff/3600., decoff/3600.)
        image = self.fitsimage.get_image()
        xc, yc = image.radectopix(self.ra_as_drawn, self.dec_as_drawn)
        xn, yn = image.radectopix(ra, dec)
        # update latest dither centre
        self.ra_as_drawn, self.dec_as_drawn = ra, dec

        obj = self.canvas.get_object_by_tag('ccd_overlay')
        obj.move_delta(xn-xc, yn-yc)
        self.canvas.update_canvas()

    def _chip_cen(self):
        """
        return chip centre in ra, dec
        """
        xoff_hpix = (self.nxtot/2 - self.rotcen_x)
        yoff_hpix = (self.nytot/2 - self.rotcen_y)
        yoff_deg = _px_deg(yoff_hpix, self.px_scale)
        xoff_deg = _px_deg(xoff_hpix, self.px_scale)

        if not self.flipEW:
            xoff_deg *= -1

        return wcs.add_offset_radec(self.ctr_ra_deg, self.ctr_dec_deg,
                                    xoff_deg, yoff_deg)

    def _make_win(self, xs, ys, nx, ny, image, **params):
        """
        Make a canvas object to represent a CCD window

        Parameters
        ----------
        xs, ys, nx, ny : float
            xstart, ystart and size in instr pixels
        image : `~ginga.AstroImage`
            image reference for calculating scales
        params : dict
            parameters passed straight through to canvas object
        Returns
        -------
        win : `~ginga.canvas.CompoundObject`
            ginga canvas object to draw on FoV
        """
        # need bottom left coord and xy size of window in degrees
        # offset of bottom left coord window from chip ctr in degrees
        xoff_hpix = (xs*u.pix - self.rotcen_x)
        yoff_hpix = (ys*u.pix - self.rotcen_y)
        yoff_deg = _px_deg(yoff_hpix, self.px_scale)
        xoff_deg = _px_deg(xoff_hpix, self.px_scale)

        if not self.flipEW:
            xoff_deg *= -1

        ll_ra, ll_dec = wcs.add_offset_radec(self.ctr_ra_deg, self.ctr_dec_deg,
                                             xoff_deg, yoff_deg)
        xsize_deg = _px_deg(nx*u.pix, self.px_scale)
        ysize_deg = _px_deg(ny*u.pix, self.px_scale)
        if not self.flipEW:
            xsize_deg *= -1
        return CCDWin(ll_ra, ll_dec, xsize_deg, ysize_deg, image, **params)

    def _make_ccd(self, image):
        """
        Converts the current instrument settings to a ginga canvas object
        """
        # get window pair object from top widget
        g = get_root(self).globals
        wframe = g.ipars.wframe

        # all values in pixel coords of the FITS frame
        # get centre
        ctr_x, ctr_y = image.radectopix(self.ctr_ra_deg, self.ctr_dec_deg)
        self.ctr_x, self.ctr_y = ctr_x, ctr_y

        nx, ny = self.nxtot.value, self.nytot.value
        mainCCD = self._make_win(0, 0, nx, ny, image,
                                 fill=True, fillcolor='blue',
                                 fillalpha=0.3, name='mainCCD')

        # dashed lines to mark quadrants of CCD
        chip_ctr_ra, chip_ctr_dec = self._chip_cen()
        xright, ytop = wcs.add_offset_radec(chip_ctr_ra, chip_ctr_dec,
                                            self.fov_x/2, self.fov_y/2)
        xleft, ybot = wcs.add_offset_radec(chip_ctr_ra, chip_ctr_dec,
                                           -self.fov_x/2, -self.fov_y/2)
        points = [image.radectopix(ra, dec) for (ra, dec) in (
            (chip_ctr_ra, ybot), (chip_ctr_ra, ytop)
        )]
        hline = Path(points, color='red', linestyle='dash', linewidth=2)
        points = [image.radectopix(ra, dec) for (ra, dec) in (
            (xleft, chip_ctr_dec), (xright, chip_ctr_dec)
        )]
        vline = Path(points, color='red', linestyle='dash', linewidth=2)

        # list of objects for compound object
        obl = [mainCCD, hline, vline]

        # iterate over window pairs
        # these coords in ccd pixel vaues
        params = dict(fill=True, fillcolor='red', fillalpha=0.3)
        if not g.ipars.isFF():
            if g.ipars.isDrift():
                for xsl, xsr, ys, nx, ny in wframe:
                    obl.append(self._make_win(xsl, ys, nx, ny, image, **params))
                    obl.append(self._make_win(xsr, ys, nx, ny, image, **params))
            else:
                for xsll, xsul, xslr, xsur, ys, nx, ny in wframe:
                    obl.append(self._make_win(xsll, ys, nx, ny, image, **params))
                    obl.append(self._make_win(xsul, 1024-ys, nx, -ny, image, **params))
                    obl.append(self._make_win(xslr, ys, nx, ny, image, **params))
                    obl.append(self._make_win(xsur, 1024-ys, nx, -ny, image, **params))

        obj = CompoundObject(*obl)
        obj.editable = True
        return obj

    def _make_compo(self, image):
        # get COMPO widget from main GUI
        g = get_root(self).globals

        compo_angle = g.compo_hw.setup_frame.pickoff_angle.value()
        compo_side = g.compo_hw.setup_frame.injection_side.value()

        # get chip coordinates - COMPO is aligned to chip
        chip_ctr_ra, chip_ctr_dec = self._chip_cen()

        if compo_side == 'R':
            ia = -INJECTOR_THETA
        elif compo_side == 'L':
            ia = INJECTOR_THETA
        else:
            ia = PARK_POSITION

        # add COMPO components
        compo_arc = CompoPatrolArc(chip_ctr_ra, chip_ctr_dec, image,
                                   linewidth=10, color='black', linestyle='dash',
                                   name='COMPO_Arc')
        compo_free = CompoFreeRegion(chip_ctr_ra, chip_ctr_dec, image,
                                     fill=True, fillcolor='green', fillalpha=0.1,
                                     name='compo_free_region')

        compo_pickoff = PickoffArm().to_ginga_object(compo_angle*u.deg, chip_ctr_ra*u.deg, chip_ctr_dec*u.deg,
                                                     fill=True, fillcolor='yellow', fillalpha=0.3,
                                                     name='COMPO_pickoff')

        compo_injector = InjectionArm().to_ginga_object(ia, chip_ctr_ra*u.deg, chip_ctr_dec*u.deg,
                                                        color='yellow', fillalpha=0.3, fill=True,
                                                        name='COMPO_injector')

        obl = [compo_arc, compo_free, compo_pickoff, compo_injector]
        obj = CompoundObject(*obl)
        obj.editable = True
        return obj

    def draw_ccd(self, *args):
        image = self.fitsimage.get_image()
        if image is None:
            return

        try:
            pa = self.pa.value() - self.paOff
            if not self.EofN:
                pa *= -1
        except Exception as err:
            errmsg = "failed to find rotation: {}".format(str(err))
            self.logger.error(errmsg)

        try:
            obj = self._make_ccd(image)
            obj.showcap = True

            self.canvas.deleteObjectByTag('ccd_overlay')
            self.canvas.add(obj, tag='ccd_overlay', redraw=False)
            # rotate
            obj.rotate(pa, self.ctr_x, self.ctr_y)
            obj.color = 'red'

            # save old values so we don't have to recompute FOV if we're just moving
            self.pa_as_drawn = pa
            self.ra_as_drawn, self.dec_as_drawn = self.ctr_ra_deg, self.ctr_dec_deg
        except Exception as err:
            errmsg = "failed to draw CCD: {}".format(str(err))
            self.logger.error(msg=errmsg)

        try:
            g = get_root(self).globals
            if g.ipars.compo():
                obj = self._make_compo(image)
                obj.showcap = True
                self.canvas.deleteObjectByTag('compo_overlay')
                self.canvas.add(obj, tag='compo_overlay', redraw=False)
                # rotate
                obj.rotate(pa, self.ctr_x, self.ctr_y)
            else:
                self.canvas.deleteObjectByTag('compo_overlay')
        except Exception as err:
            errmsg = "failed to draw COMPO: {}".format(str(err))
            self.logger.error(msg=errmsg)

        self.canvas.update_canvas()

    def create_blank_image(self):
        self.fitsimage.onscreen_message("Creating blank field...",
                                        delay=1.0)
        image = dp.create_blank_image(self.ctr_ra_deg, self.ctr_dec_deg,
                                      2*self.fov,
                                      0.000047, 0.0,
                                      cdbase=[-1, 1],
                                      logger=self.logger)
        image.set(nothumb=True)
        self.fitsimage.set_image(image)

    def set_and_load(self):
        coo = SkyCoord(self.targCoords.value(),
                       unit=(u.hour, u.deg))
        self.ra.set(coo.ra.deg)
        self.dec.set(coo.dec.deg)
        self.load_image()

    def load_image(self):
        self.fitsimage.onscreen_message("Getting image; please wait...")
        # offload to non-GUI thread to keep viewer somewhat responsive?
        t = threading.Thread(target=self._load_image)
        t.daemon = True
        self.logger.debug(msg='starting image download')
        t.start()
        self.after(1000, self._check_image_load, t)

    def _check_image_load(self, t):
        if t.isAlive():
            self.logger.debug(msg='checking if image has arrrived')
            self.after(500, self._check_image_load, t)
        else:
            # load image into viewer
            try:
                get_root(self).load_file(self.imfilepath)
            except Exception as err:
                errmsg = "failed to load file {}: {}".format(
                    self.imfilepath,
                    str(err)
                )
                self.logger.error(msg=errmsg)
            else:
                self.draw_ccd()
                self.targetMarker()
            finally:
                self.fitsimage.onscreen_message(None)

    def _load_image(self):
        try:
            fov_deg = 5*max(self.fov_x, self.fov_y)
            ra_txt = self.ra.as_string()
            dec_txt = self.dec.as_string()
            # width and height are specified in arcmin
            wd = 60*fov_deg
            ht = 60*fov_deg

            # these are the params to DSS
            params = dict(ra=ra_txt, dec=dec_txt, width=wd, height=ht)

            # query server and download file
            filename = 'sky.fits'
            filepath = os.path.join(self.tmpdir, filename)
            if os.path.exists(filepath):
                os.unlink(filepath)
            print(self.servername, self.bank.getServerNames())
            dstpath = self.bank.getImage(self.servername, filepath, **params)
        except Exception as err:
            errmsg = "Failed to download sky image: {}".format(str(err))
            self.logger.error(msg=errmsg)
            return

        self.imfilepath = dstpath
