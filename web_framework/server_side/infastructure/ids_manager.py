from __future__ import annotations
import uuid
from typing import TYPE_CHECKING
from typing import List, Dict, Callable
if TYPE_CHECKING:
    from web_framework.server_side.infastructure.ui_component import UIComponent

component_ids: Dict[str, UIComponent] = {}
action_ids: Dict[str, Callable] = {}

def gen_component_id(component: UIComponent):
    """
    Generate a new, unique, component ID
    """
    comp_id = str(uuid.uuid4())
    #while comp_id in component_ids:
    #    comp_id = str(uuid.uuid4())
    
    component_ids[comp_id] = component
    return comp_id

def gen_action_id(action):
    """
    Generate a new, unique, action ID
    """
    action_id = str(uuid.uuid4())
    #while action_id in action_ids:
    #    action_id = str(uuid.uuid4())
    
    action_ids[action_id] = action
    return action_id
