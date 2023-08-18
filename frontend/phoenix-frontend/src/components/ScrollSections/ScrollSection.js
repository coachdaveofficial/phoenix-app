import React from 'react';
import './ScrollSection.css';

export default function ScrollSection({sectionId, text, bgColor}) {
    return (
        <div style={{backgroundColor: `${bgColor}`}} className="scroll-section" id={sectionId}>
            {text}
        </div>
    )
}