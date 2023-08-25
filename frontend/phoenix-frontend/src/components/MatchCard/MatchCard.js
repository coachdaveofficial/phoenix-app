import React, { useState } from 'react';
import Tab from './Tab';
import CardContent from './CardContent';


const logoUrl = 'https://scontent.fhio2-2.fna.fbcdn.net/v/t39.30808-6/327021022_495844319156343_4404772642969112146_n.jpg?_nc_cat=109&ccb=1-7&_nc_sid=09cbfe&_nc_ohc=G6_0DOJyr_sAX-OhW0_&_nc_ht=scontent.fhio2-2.fna&oh=00_AfC-ws7dDX3umOjvBheZBO-cr8nZgSGeTqZF7jqtiRDTXQ&oe=64E50846'

export default function MatchCard() {
    const [activeTab, setActiveTab] = useState('Upcoming');

    const handleTabClick = (tab) => {
        setActiveTab(tab);
    };

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
                <CardContent isActive={activeTab === 'Upcoming'} phoenixLogo={logoUrl} phoenixTeam={"Open"} opposingTeam={"Test FC"}>
                    
                </CardContent>
                <CardContent isActive={activeTab === 'Previous'}>
                </CardContent>
                <CardContent isActive={activeTab === 'History'}>
                </CardContent>
            </div>
        </div>
    );
};


