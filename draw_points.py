# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DrawPoints
                                 A QGIS plugin
 This plugin draw points.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-07-19
        git sha              : $Format:%H$
        copyright            : (C) 2022 by SIGMA
        email                : info@sigma-geophys.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .draw_points_dialog import DrawPointsDialog
import os.path


class DrawPoints:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'DrawPoints_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Draw Points')
        self.dlg = DrawPointsDialog()

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

        self.dlg.choose_button.clicked.connect(self.choose_menu_show)
        # меню выбора штучек
        self.dlg.choose_grid_button.clicked.connect(self.click_choose_grid)
        self.dlg.choose_gridslope_button.clicked.connect(self.click_choose_gridslope)
        self.dlg.choose_snow_button.clicked.connect(self.click_choose_snow)
        self.dlg.choose_snowadvanced_button.clicked.connect(self.click_choose_snowadvanced)



    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('DrawPoints', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/draw_points/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Draw points'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Draw Points'),
                action)
            self.iface.removeToolBarIcon(action)

    def grid_hide(self):
        self.dlg.grid_height_label.hide()
        self.dlg.grid_height.hide()
        self.dlg.grid_lenght_label.hide()
        self.dlg.grid_lenght.hide()
        self.dlg.grid_vertical_lines_amount_label.hide()
        self.dlg.grid_vertical_lines_amount.hide()
        self.dlg.grid_horizontal_lines_amount_label.hide()
        self.dlg.grid_horizontal_lines_amount.hide()
        self.dlg.grid_coords_of_left_bottom_corner_label.hide()
        self.dlg.grid_coords_of_left_bottom_corner.hide()
        self.dlg.grid_system_of_coords_label.hide()
        self.dlg.grid_system_of_coords.hide()
        self.dlg.grid_frame.hide()

    def grid_show(self):
        self.dlg.grid_height_label.show()
        self.dlg.grid_height.show()
        self.dlg.grid_lenght_label.show()
        self.dlg.grid_lenght.show()
        self.dlg.grid_vertical_lines_amount_label.show()
        self.dlg.grid_vertical_lines_amount.show()
        self.dlg.grid_horizontal_lines_amount_label.show()
        self.dlg.grid_horizontal_lines_amount.show()
        self.dlg.grid_coords_of_left_bottom_corner_label.show()
        self.dlg.grid_coords_of_left_bottom_corner.show()
        self.dlg.grid_system_of_coords_label.show()
        self.dlg.grid_system_of_coords.show()
        self.dlg.grid_frame.show()

    def gridslope_hide(self):
        self.dlg.gridslope_height_label.hide()
        self.dlg.gridslope_height.hide()
        self.dlg.gridslope_lenght_label.hide()
        self.dlg.gridslope_lenght.hide()
        self.dlg.gridslope_vertical_lines_amount_label.hide()
        self.dlg.gridslope_vertical_lines_amount.hide()
        self.dlg.gridslope_horizontal_lines_amount_label.hide()
        self.dlg.gridslope_horizontal_lines_amount.hide()
        self.dlg.gridslope_coords_of_left_bottom_corner_label.hide()
        self.dlg.gridslope_coords_of_left_bottom_corner.hide()
        self.dlg.gridslope_system_of_coords_label.hide()
        self.dlg.gridslope_system_of_coords.hide()
        self.dlg.gridslope_frame.hide()

    def gridslope_show(self):
        self.dlg.gridslope_height_label.show()
        self.dlg.gridslope_height.show()
        self.dlg.gridslope_lenght_label.show()
        self.dlg.gridslope_lenght.show()
        self.dlg.gridslope_vertical_lines_amount_label.show()
        self.dlg.gridslope_vertical_lines_amount.show()
        self.dlg.gridslope_horizontal_lines_amount_label.show()
        self.dlg.gridslope_horizontal_lines_amount.show()
        self.dlg.gridslope_coords_of_left_bottom_corner_label.show()
        self.dlg.gridslope_coords_of_left_bottom_corner.show()
        self.dlg.gridslope_system_of_coords_label.show()
        self.dlg.gridslope_system_of_coords.show()
        self.dlg.gridslope_frame.show()

    def snow_hide(self):
        self.dlg.snow_radius_label.hide()
        self.dlg.snow_radius.hide()
        self.dlg.snow_lines_amount_label.hide()
        self.dlg.snow_lines_amount.hide()
        self.dlg.snow_gap_label.hide()
        self.dlg.snow_gap.hide()
        self.dlg.snow_coords_of_center_label.hide()
        self.dlg.snow_coords_of_center.hide()
        self.dlg.snow_system_of_coords_label.hide()
        self.dlg.snow_system_of_coords.hide()
        self.dlg.snow_frame.hide()

    def snow_show(self):
        self.dlg.snow_radius_label.show()
        self.dlg.snow_radius.show()
        self.dlg.snow_lines_amount_label.show()
        self.dlg.snow_lines_amount.show()
        self.dlg.snow_gap_label.show()
        self.dlg.snow_gap.show()
        self.dlg.snow_coords_of_center_label.show()
        self.dlg.snow_coords_of_center.show()
        self.dlg.snow_system_of_coords_label.show()
        self.dlg.snow_system_of_coords.show()
        self.dlg.snow_frame.show()

    def snowadvanced_hide(self):
        self.dlg.snowadvanced_radius_label.hide()
        self.dlg.snowadvanced_radius.hide()
        self.dlg.snowadvanced_lines_amount_label.hide()
        self.dlg.snowadvanced_lines_amount.hide()
        self.dlg.snowadvanced_gap_label.hide()
        self.dlg.snowadvanced_gap.hide()
        self.dlg.snowadvanced_coords_of_center_label.hide()
        self.dlg.snowadvanced_coords_of_center.hide()
        self.dlg.snowadvanced_system_of_coords_label.hide()
        self.dlg.snowadvanced_system_of_coords.hide()
        self.dlg.snowadvanced_frame.hide()

    def snowadvanced_show(self):
        self.dlg.snowadvanced_radius_label.show()
        self.dlg.snowadvanced_radius.show()
        self.dlg.snowadvanced_lines_amount_label.show()
        self.dlg.snowadvanced_lines_amount.show()
        self.dlg.snowadvanced_gap_label.show()
        self.dlg.snowadvanced_gap.show()
        self.dlg.snowadvanced_coords_of_center_label.show()
        self.dlg.snowadvanced_coords_of_center.show()
        self.dlg.snowadvanced_system_of_coords_label.show()
        self.dlg.snowadvanced_system_of_coords.show()
        self.dlg.snowadvanced_frame.show()

    def choose_menu_hide(self):
        self.dlg.background_for_choose_menu.hide()
        self.dlg.choose_grid_button.hide()
        self.dlg.choose_gridslope_button.hide()
        self.dlg.choose_snow_button.hide()
        self.dlg.choose_snowadvanced_button.hide()
        self.dlg.choose_frame.hide()

    def choose_menu_show(self):
        self.clear_types_input()
        self.dlg.background_for_choose_menu.show()
        self.dlg.choose_grid_button.show()
        self.dlg.choose_gridslope_button.show()
        self.dlg.choose_snow_button.show()
        self.dlg.choose_snowadvanced_button.show()
        self.dlg.choose_frame.show()

    def clear_types_input(self):
        self.grid_hide()
        self.gridslope_hide()
        self.snow_hide()
        self.snowadvanced_hide()

    def click_choose_grid(self):
        self.choose_menu_hide()
        self.clear_types_input()
        self.grid_show()
        self.dlg.openGLWidget.show()

    def click_choose_gridslope(self):
        self.choose_menu_hide()
        self.clear_types_input()
        self.gridslope_show()
        self.dlg.openGLWidget.show()

    def click_choose_snow(self):
        self.choose_menu_hide()
        self.clear_types_input()
        self.snow_show()
        self.dlg.openGLWidget.show()

    def click_choose_snowadvanced(self):
        self.choose_menu_hide()
        self.clear_types_input()
        self.snowadvanced_show()
        self.dlg.openGLWidget.show()

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started


        # show the dialog
        self.dlg.show()

        self.grid_hide()
        self.gridslope_hide()
        self.snow_hide()
        self.dlg.openGLWidget.hide()
        self.choose_menu_hide()
        self.snowadvanced_hide()
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

