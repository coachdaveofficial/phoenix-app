import React, { useEffect, useState } from 'react';
import Tab from './Tab';
import MatchCardContent from './MatchCardContent'
import PlayerStatsCardContent from './PlayerStatsCardContent';
import organizeMatchData from '@/helpers/organizeMatchData';
import { PropagateLoader } from 'react-spinners';


const logoUrl = '/phoenixfc_logo.jpeg'

export default function MatchCard({ phoenixTeam, teamData }) {
    const [activeTab, setActiveTab] = useState('Upcoming');
    const [loading, setLoading] = useState(true);


    const prevData = organizeMatchData(teamData.prev_match);
    const upcomingData = organizeMatchData(teamData.upcoming_match);
    const mostGoalsAndAssistsData = { mostGoals: teamData.most_goals, mostAssists: teamData.most_assists };
    const recentSeasonRecords = {
        mostGoals: teamData.recent_goals,
        mostAssists: teamData.recent_assists,
        season: teamData.recent_season
    };
    setLoading(false);


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
                    <option>Player Stats</option>
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
                            label="Player Stats"
                            isActive={activeTab === 'Player Stats'}
                            onClick={() => handleTabClick('Player Stats')}
                        />
                    </li>
                </ul>
            </div>
            {/* Card Content below */}
            <div className="">
                {upcomingData ?
                    <MatchCardContent
                        isActive={activeTab === 'Upcoming'}
                        phoenixLogo={logoUrl}
                        phoenixTeam={phoenixTeam}
                        opposingTeam={upcomingData.opposingTeam.name}
                        location={upcomingData.location}
                        date={upcomingData.date}
                        time={upcomingData.time}

                    />
                    :
                    <MatchCardContent
                        isActive={activeTab === 'Upcoming'}
                        loading={loading}
                        phoenixLogo={logoUrl}
                        phoenixTeam={phoenixTeam}
                        opposingTeam={"Unknown"}
                    />
                }
                {prevData ?
                    <MatchCardContent
                        isActive={activeTab === 'Previous'}
                        loading={loading}
                        phoenixLogo={logoUrl}
                        phoenixTeam={phoenixTeam}
                        opposingTeam={prevData.opposingTeam.name}
                        score={prevData.score}
                        location={prevData.location}
                        date={prevData.date}
                        time={prevData.time}
                        goals={prevData.goals}
                        loadIcon={PropagateLoader}
                    />
                    :
                    <MatchCardContent
                        isActive={activeTab === 'Previous'}
                        loading={loading}
                        phoenixLogo={logoUrl}

                    />

                }
                {mostGoalsAndAssistsData &&
                    <PlayerStatsCardContent
                        isActive={activeTab === 'Player Stats'}
                        loading={loading}
                        allTimeGoalScorers={mostGoalsAndAssistsData.mostGoals}
                        allTimeAssisters={mostGoalsAndAssistsData.mostAssists}
                        recentSeasonTopScorers={recentSeasonRecords.mostGoals}
                        recentSeasonMostAssists={recentSeasonRecords.mostAssists}
                        recentSeason={recentSeasonRecords.season}

                    />


                }
            </div>
        </div>
    );
};


