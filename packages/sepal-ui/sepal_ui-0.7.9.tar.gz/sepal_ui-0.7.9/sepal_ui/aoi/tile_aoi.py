from functools import partial

import ipyvuetify as v
import geemap
import ee

from .aoi_io import Aoi_io
from .. import sepalwidgets as sw
from ..scripts import utils as su, run_aoi_selection
from ..mapping import SepalMap

if not ee.data._credentials: ee.Initialize()
    
class FileNameField(v.TextField, sw.SepalWidget):
    
    def __init__(self, default_name = ''):
        
        super().__init__(
            label   = 'Select a filename', 
            v_model = default_name
        )
        
class CountrySelect(v.Select, sw.SepalWidget):
    
    def __init__(self):
        
        super().__init__(
            items   = [*su.create_FIPS_dic()], 
            label   = 'Country/Province', 
            v_model = None
        )
        
class TileAoi(sw.Tile):
    """render and bind all the variable to create an autonomous aoi selector. It will create a asset in you gee account with the name 'aoi_[aoi_name]'. The assetId will be added to io.assetId.
    
    available selection methods : 'Country boundaries', 'Draw a shape', 'Upload file', 'Use GEE asset', 'Use points file'
    """
    
    # constants
    SELECTION_METHOD =('Country boundaries', 'Draw a shape', 'Upload file', 'Use GEE asset', 'Use points file')
    
    def __init__(self, io, methods = SELECTION_METHOD, **kwargs):
        
        # create the output
        aoi_output = sw.Alert()#.add_msg(ms.AOI_MESSAGE)
        
        # create the inputs widgets 
        aoi_file_input = sw.FileInput(['.shp']).hide()
        aoi_output.bind(aoi_file_input, io, 'file_input')
    
        aoi_file_name = FileNameField(io.file_name).hide()
        aoi_output.bind(aoi_file_name, io, 'file_name')
    
        aoi_country_selection = CountrySelect().hide()
        aoi_output.bind(aoi_country_selection, io, 'country_selection')
    
        aoi_asset_name = sw.AssetSelect().hide()
        aoi_output.bind(aoi_asset_name, io, 'assetId')
        
        aoi_load_table = sw.LoadTableField().hide()
        aoi_output.bind(aoi_load_table, io, 'json_csv')
    
        widget_list = [
            aoi_file_input, 
            aoi_file_name, 
            aoi_country_selection, 
            aoi_asset_name,
            aoi_load_table
        ]
        
        #create the map 
        m = SepalMap(['Esri Satellite', 'CartoDB.Positron'], dc=True)
        self.handle_draw(m.dc, io, 'drawn_feat', aoi_output)
    
        #bind the input to the selected method 
        method_items = [m for m in methods if m in self.SELECTION_METHOD] 
        aoi_select_method = v.Select(items = method_items, label = 'AOI selection method', v_model = None)
        self.bind_aoi_method(aoi_select_method, widget_list, io, m, self.SELECTION_METHOD)
    

        # create the validation button 
        aoi_select_btn = sw.Btn('Select these inputs')
        self.bind_aoi_process(aoi_select_btn, io, m, aoi_output, self.SELECTION_METHOD)
    
        # assemble everything on a tile 
        inputs = v.Layout(
            _metadata    = {'mount-id': 'data-input'},
            class_       = "pa-5",
            row          = True,
            align_center = True, 
            children     = (
                [v.Flex(xs12 = True, children =[aoi_select_method])] 
                + [v.Flex(xs12 = True, children = [widget]) for widget in widget_list]
                + [v.Flex(xs12 = True, children =[aoi_select_btn])] 
                + [v.Flex(xs12 = True, children = [aoi_output])]
            )
        )
        
        aoi_content_main = v.Layout(
            row      = True,
            xs12     = True,
            children = [
                v.Flex(xs12 = True, md6 = True, children = [inputs]),
                v.Flex(xs12 = True, md6 = True, class_ = "pa-5", children = [m])
            ]
        )
        
        super().__init__(id_ = 'aoi_widget', title = 'AOI selection', inputs = [aoi_content_main])
        
    def handle_draw(self, dc, io, variable, output):
        """ 
        handle the drawing of a geometry on a map. The geometry is transform into a ee.featurecollection and send to the variable attribute of obj.
    
        Args: 
            dc (DrawControl) : the draw control on which the drawing will be done 
            io (obj Aoi_io) : any object created for IO of your tile 
            variable (str) : the name of the atrribute of the obj object where to store the ee.FeatureCollection 
            output (sw.Alert) : the output to display results
        
    """
        def on_draw(self, action, geo_json, obj, variable, output):
            geom = geemap.geojson_to_ee(geo_json, False)
            feature = ee.Feature(geom)
            setattr(obj, variable, ee.FeatureCollection(feature)) 
            
            output.add_live_msg('A shape have been drawn')

            return 
        
        dc.on_draw(partial(
            on_draw,
            obj=io,
            variable=variable,
            output=output
        ))
    
        return self
    
    def bind_aoi_process(self, btn, io, m, output, list_method):
        """
        Create an asset in your gee acount and serve it to the map.
        
        Args:
            btn (v.Btn) : the btn that launch the process
            io (Aoi_IO) : the IO of the aoi selection tile
            m (geemap.Map) : the tile map
            dc (drawcontrol) : the drawcontrol
            output (v.Alert) : the alert of the selector tile
            list_method([str]) : the list of the available selections methods
        """
    
        def on_click(widget, event, data, io, m, output, list_method):
        
            widget.toggle_loading()            
            
            try:
                # create the aoi asset
                run_aoi_selection.run_aoi_selection(
                    output      = output, 
                    list_method = list_method, 
                    io          = io
                )
                
                # hide the drawing control 
                m.hide_dc()
        
                # display the resulting aoi on the map
                io.display_on_map(m)
                
            except Exception as e: 
                output.add_live_msg(str(e), 'error') 
            
            widget.toggle_loading()
        
            return 
    
        btn.on_event('click', partial(
            on_click,
            io          = io, 
            m           = m,
            output      = output,
            list_method = list_method
        ))
    
        return self
    
    def bind_aoi_method(self, method_widget, list_input, obj, m, selection_method):
        """
        change the display of the AOI selector according to the method selected. will only display the useful one
        
        Args: 
            method_widget (v.select) : the method selector widget 
            list_input ([v.widget]) : the list of all the aoi inputs
            obj (Aoi_IO) : the IO object of the tile
            m (geemap.Map) the map displayed in the tile
            dc (DrawControl) : the drawing control
            selection_method ([str]) : the available selection methods
        """
        
        
        def on_change(widget, event, data, list_input, obj, m, selection_method):
            
            # clearly identify the differents widgets 
            aoi_file_input        = list_input[0]
            aoi_file_name         = list_input[1]
            aoi_country_selection = list_input[2]
            aoi_asset_name        = list_input[3]
            aoi_load_table        = list_input[4]
            
            setattr(obj, 'selection_method', widget.v_model)
            
            m.hide_dc()
                
            # toogle the appropriate inputs
            if widget.v_model == selection_method[0]: # country selection
                self.toggle_inputs([aoi_country_selection], list_input)
            elif widget.v_model == selection_method[1]: # drawing
                self.toggle_inputs([aoi_file_name], list_input)
                m.show_dc()
            elif widget.v_model == selection_method[2]: # shp file
                self.toggle_inputs([aoi_file_input], list_input)
            elif widget.v_model == selection_method[3]: # gee asset
                self.toggle_inputs([aoi_asset_name], list_input)
            elif widget.v_model == selection_method[4]: # Point file (.csv)
                self.toggle_inputs([aoi_load_table], list_input)
            else:
                self.toggle_inputs([], list_input)
                
        method_widget.on_event('change', partial(
            on_change,
            list_input       = list_input,
            obj              = obj,
            m                = m, 
            selection_method = selection_method
        ))
        
        return self 