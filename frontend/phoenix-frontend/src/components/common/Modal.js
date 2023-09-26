import React from "react";

export default function Modal({ children, handleModalShow, title }) {
    return (
        <div
            id=""
            tabIndex="-1"
            aria-hidden="true"
            className="modal fixed top-0 left-0 right-0 z-50 flex justify-center items-center h-screen w-full p-4 overflow-x-hidden overflow-y-auto bg-gray-900 bg-opacity-50"
        >
            <div className="relative w-full max-w-md">
                {/* Modal content */}
                <div className="relative rounded-lg shadow bg-gray-700">
                    
                    <button
                        type="button"
                        className="absolute top-3 right-2.5 text-gray-400 bg-transparent rounded-lg text-sm w-8 h-8 ml-auto inline-flex justify-center items-center hover:bg-gray-600 hover:text-white"
                        onClick={handleModalShow}
                    >
                        <svg
                            className="w-3 h-3"
                            aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg"
                            fill="none"
                            viewBox="0 0 14 14"
                        >
                            <path
                                stroke="currentColor"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth="2"
                                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"
                            />
                        </svg>
                        <span className="sr-only">Close modal</span>
                    </button>
                    <div className="px-6 py-6 lg:px-8">
                        <h3 className="mb-4 text-xl font-medium text-white">{title}</h3>
                        {children}
                    </div>
                </div>
            </div>
        </div>
    );
}
