import React, { useState, useEffect } from 'react'
import axios from "axios";
import Alert from '../common/Alert';
export default function ScriptForm({handleRefresh}) {
    
    const API_BASE_URL = 'http://127.0.0.1:8080/api'
    const INITIAL_STATE = {
        worksheet: "",
        year: "",
        season: "",
        team_type: "Open"
    }
    const [formData, setFormData] = useState(INITIAL_STATE)
    const [formErrors, setFormErrors] = useState([])
    const [formSuccessMsg, setFormSuccessMsg] = useState([])

    const handleChange = (evt) => {
        const { name, value } = evt.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value
        }));
    }

    const handleSubmit = async (evt) => {
        evt.preventDefault();
        try {
            let result = await axios.post(`${API_BASE_URL}/script/`, formData, { withCredentials: true });
            console.log(result)
            if (result.status === 201) {
                console.log("success")
                setFormSuccessMsg([result.data.message]);
                setFormData(INITIAL_STATE);
                setFormErrors([]);
                handleRefresh();

            }
        } catch (e) {
            console.log(e);
            setFormErrors([e.response.data.message])
        }


    }

    return (
        <>

            <form className="space-y-6" method="" onSubmit={handleSubmit}>
                <div className="mb-6">
                    <label htmlFor="worksheet" className="block mb-2 text-sm font-medium text-white">Worksheet Name</label>
                    <input type="text" id="worksheet"
                        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                        name="worksheet"
                        value={formData.worksheet}
                        onChange={handleChange}
                        required />
                </div>
                <div className="mb-6">
                    <label htmlFor="year" className="block mb-2 text-sm font-medium text-white">Year</label>
                    <input type="text" id="year"
                        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                        name="year"
                        value={formData.year}
                        onChange={handleChange}
                        required />
                </div>
                <div className="mb-6">
                    <label htmlFor="season" className="block mb-2 text-sm font-medium text-white">Season</label>
                    <input type="text" id="season"
                        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                        name="season"
                        value={formData.season}
                        onChange={handleChange}
                        required />
                </div>
                <div className="mb-6">
                    <label htmlFor="team_type" className="block mb-2 text-sm font-medium text-white">Phoenix Team</label>
                    <select
                        id="team_type"
                        className="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
                        name="team_type"
                        value={formData.team_type}
                        onChange={handleChange}
                        required
                    >
                        <option value="Open">Open</option>
                        <option value="O30">O30</option>
                        <option value="O40">O40</option>
                    </select>

                </div>
                {formErrors.length
                    ? <Alert type="danger" messages={formErrors} />
                    : null}
                {formSuccessMsg.length
                    ? <Alert type="success" messages={formSuccessMsg} />
                    :
                    null}
                <button type="submit" className="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Submit</button>
            </form>

        </>

    )
}