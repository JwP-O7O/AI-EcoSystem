import React from 'react';

interface IconProps {
    icon: any; // Loosened type for safety
    className?: string;
}

const Icon: React.FC<IconProps> = ({ icon, className }) => {
    if (!icon) return null;

    // If it's a valid element (like the SVGs in constants), clone it with new className
    if (React.isValidElement(icon)) {
        // Merge existing className with new one
        const existingClass = icon.props.className || '';
        const newClass = className ? `${existingClass} ${className}`.trim() : existingClass;
        
        return React.cloneElement(icon as React.ReactElement, {
            className: newClass,
        });
    }
    
    return null;
};

export default Icon;