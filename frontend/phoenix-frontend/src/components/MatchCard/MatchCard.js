import React, { useEffect, useState } from 'react';
import Tab from './Tab';
import CardContent from './CardContent';
import organizeMatchData from '@/helpers/organizeMatchData';


const logoUrl = '/phoenixfc_logo.jpeg'

import axios from "axios";
const API_BASE_URL = 'http://127.0.0.1:8080/api';

export default function MatchCard({phoenixTeam}) {
    const [activeTab, setActiveTab] = useState('Upcoming');
    const [prevData, setPrevData] = useState(null);
    const [upcomingData, setUpcomingData] = useState(null);

    const handleTabClick = (tab) => {
        setActiveTab(tab);
    };

    useEffect(() => {
        const getTeamData = async () => {
            const phoenixTeamResp = await axios.get(`${API_BASE_URL}/teams/?name=${phoenixTeam}`);
            const phoenixTeamObj = phoenixTeamResp.data[0];
            console.log(phoenixTeamObj)
            const prevMatchResp = await axios.get(`${API_BASE_URL}/matches/${phoenixTeamObj.id}/previous`);
            setPrevData(organizeMatchData(prevMatchResp.data));

            try {
                const upcomingMatchResp = await axios.get(`${API_BASE_URL}/matches/${phoenixTeamObj.id}/upcoming`);
                console.log(upcomingData)
                setUpcomingData(organizeMatchData(upcomingMatchResp))
            } catch (e) {
                setUpcomingData(false)
            }

        }
        getTeamData();
    }, [])

    return (
        <div className="w-full bg-white border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700">
            <div className="flex lg:hidden">
                <label htmlFor="tabs" className="sr-only">
                    Select tab
                </label>
                <select value={activeTab} onChange={e => setActiveTab(e.target.value)} id="tabs" className="bg-gray-50 border-0 border-b border-gray-200 text-gray-900 text-xs rounded-t-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 break-words">
                    <option>Upcoming</option>
                    <option>Previous</option>
                    <option>History</option>
                </select>
            </div>
            <div className="hidden lg:block">
                <ul className="hidden text-sm font-medium text-center text-gray-500 divide-x divide-gray-200 rounded-lg sm:flex dark:divide-gray-600 dark:text-gray-400" id="fullWidthTab" data-tabs-toggle="#fullWidthCardContent" role="tablist">
                    <li className="w-full">
                        <Tab
                            label="Upcoming"
                            isActive={activeTab === 'Upcoming'}
                            onClick={() => handleTabClick('Upcoming')}
                        />
                    </li>
                    <li className="w-full">
                        <Tab
                            label="Previous"
                            isActive={activeTab === 'Previous'}
                            onClick={() => handleTabClick('Previous')}
                        />
                    </li>
                    <li className="w-full">
                        <Tab
                            label="History"
                            isActive={activeTab === 'History'}
                            onClick={() => handleTabClick('History')}
                        />
                    </li>
                </ul>
            </div>
            <div className="">
            {upcomingData ? 
                    <CardContent 
                        isActive={activeTab === 'Upcoming'} 
                        phoenixLogo={logoUrl} 
                        phoenixTeam={phoenixTeam} 
                        opposingTeam={prevData.opposingTeam.name}
                        score={`${prevData.score}`} 
                        location={prevData.location}
                        date={prevData.date}
                        time={prevData.time}
                    /> 
                    :
                    <CardContent 
                        isActive={activeTab === 'Upcoming'} 
                        phoenixLogo={logoUrl} 
                        phoenixTeam={phoenixTeam} 
                        // opposingTeam={prevData.opposingTeam.name}
                        // score={`${prevData.score}`} 
                        location={"no info yet"}
                        // date={prevData.date}
                        // time={prevData.time}
                    /> 
                }
                {prevData && 
                    <CardContent 
                        isActive={activeTab === 'Previous'} 
                        phoenixLogo={logoUrl} 
                        phoenixTeam={phoenixTeam} 
                        opposingTeam={prevData.opposingTeam.name}
                        score={`${prevData.score}`} 
                        location={prevData.location}
                        date={prevData.date}
                        time={prevData.time}
                    />
                }
                <CardContent isActive={activeTab === 'History'}>
                </CardContent>
            </div>
        </div>
    );
};


