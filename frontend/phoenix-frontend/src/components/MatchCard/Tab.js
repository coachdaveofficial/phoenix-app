import React from 'react';

export default function Tab({ label, isActive, onClick }) {
    return (
        <button
            className={`p-4 ${
                isActive ? 'inline-block w-full p-4 rounded-tl-lg bg-gray-50 hover:bg-gray-100 focus:outline-none dark:bg-gray-700 dark:hover:bg-gray-600' : 'bg-gray-50 dark:bg-gray-800'
            }`}
            onClick={onClick}
        >
            {label}
        </button>
    );
};