import React from 'react';
import './ScrollSection.css';

export default function ScrollSectionAbout({sectionId, text, bgColor, children}) {
    return (
        <div style={{backgroundColor: `${bgColor}`}} className="scroll-section p-4 content-start" id={sectionId}>
            {children}
        </div>
    )
}