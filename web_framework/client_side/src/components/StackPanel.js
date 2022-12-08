import React from 'react';
import ComponentSelector from "./ComponentSelector";


const StackPanel = ({children, orientation='vertical'}) => {
    const direction_s = orientation === 1 ? 'column' : 'row';
    const direction_rtl = orientation === 1 ? 'ltr' : 'rtl';
    const flex_container = {
        display: 'flex',
        flexDirection: direction_s,
        alignItems: 'center',
        justifyContent: 'center',
        height: 'fit-content'
    };

    return <div style={flex_container} id="StackPanel" dir="rtl">
        {children && children.map(child => {
                if (!child || !child.component)
                    return;
                const {component: componentData} = child;
                console.log(componentData.relative_width);
                const component = ComponentSelector(componentData);
                return <div style={{margin: '2px', width: componentData.relative_width}}>{component}</div>
            }
        )}
    </div>;
};

export default StackPanel;
