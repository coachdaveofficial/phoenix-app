import React, { useState, useEffect } from 'react'

import axios from "axios";
const API_BASE_URL = 'http://127.0.0.1:8080/auth';

export default function LoginForm({ login }) {

    const INITIAL_STATE = {
        username: "admin",
        password: "admin"
    }
    const [formData, setFormData] = useState(INITIAL_STATE)
    const [formErrors, setFormErrors] = useState([])

    useEffect(() => {
        const loginTest = async () => {
            try {
                const check = await axios.get(`${API_BASE_URL}/@me`);
                console.log(check)
            } catch (e) {
                console.log(e)
            }

        }
        loginTest()
    }, [formData])

    const handleChange = (evt) => {
        const { name, value } = evt.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value
        }));
    }

    const handleSubmit = async (evt) => {
        evt.preventDefault();

        let result = await login(formData);
        if (result.status === 200) {
            console.log("success login")
        } else {
            console.log(result.response.data.message)
            setFormErrors(result.response.data.message)
        }
    }

    return (
        <>

            <form method="" onSubmit={handleSubmit}>
                <div className="mb-6">
                    <label htmlFor="username" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Username</label>
                    <input type="text" id="username"
                        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        name="username"
                        value={formData.username}
                        onChange={handleChange}
                        required />
                </div>
                <div className="mb-6">
                    <label htmlFor="password" className="block mb-2 text-sm font-medium text-gray-900 dark:text-white">Password</label>
                    <input type="password" id="password"
                        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        name="password"
                        value={formData.password}
                        onChange={handleChange}
                        required />
                </div>
                <button type="submit" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit</button>
            </form>

        </>

    )
}