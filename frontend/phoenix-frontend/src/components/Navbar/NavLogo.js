import React from 'react'

export default function NavLogo({ imgSrc, text, path, altText }) {
    return (
        <a href={path ? path : '#'} className="flex items-center">
            <img src={imgSrc} className="h-14 mr-3 rounded-full" alt={altText} />
            <span className="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">{text}</span>
        </a>
    )
}