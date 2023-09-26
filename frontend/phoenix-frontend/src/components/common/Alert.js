import React from 'react';

export default function Alert({ type = "danger", messages = [] }) {
    console.debug("Alert", "type=", type, "messages=", messages);


    const alertClasses = {
        'danger': 'bg-red-300 text-red-800',
        'success': 'bg-green-300 text-green-800',
    };

    const alertClass = alertClasses[type] || 'bg-gray-100 text-gray-800';

    return (
        <div className={`p-4 mb-4 text-sm rounded-lg ${alertClass}`} role="alert">
            {messages.map((error, index) => (
            <p className="mb-2 font-medium" key={index}>
                {error}
            </p>
        ))}
        </div>
            
    );
}
