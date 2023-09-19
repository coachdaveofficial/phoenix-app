import React from 'react';
import { PropagateLoader } from 'react-spinners';

const titleClass = "text-xl font-semibold mb-4";
const listItemClass = "mb-2 p-2 bg-gray-100 dark:bg-gray-700 rounded-lg";

export default function PlayerStatsCardContent({ isActive, loading, allTimeGoalScorers, allTimeAssisters, recentSeasonTopScorers, recentSeasonMostAssists }) {
    
    return isActive && (

        <>
            {loading ? (
                <div className="p-4 bg-white dark:bg-gray-800 rounded-lg ">
                    <div className='grid my-6 justify-center'>
                        <div>
                            <PropagateLoader color="#ff8200" />
                        </div>

                    </div>
                </div>
            ) : (
                <div className="p-4 bg-white dark:bg-gray-800 rounded-lg 
                grid  xs:grid-cols-1  gap-2 p-4 content-start">
                    <div>
                        <h2 className={titleClass}>All-Time Most Goals</h2>
                        <ul className="list-disc pl-4">
                            {allTimeGoalScorers && allTimeGoalScorers.map((player, idx) => (
                                <li key={idx} className={listItemClass}>
                                    <div className="flex justify-between">
                                        <span>{player.player_name}</span>
                                        <span className="font-semibold">{player.goals} goals</span>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </div>

                    <div>
                        <h2 className={titleClass}>{recentSeasonTopScorers.season.name} Most Goals</h2>
                        <ul className="list-disc pl-4">
                            {/* check to see if data is an array of players */}
                            {/* if data is not array, then there are no data for this season, display error message */}
                            {Array.isArray(recentSeasonTopScorers.data) ?
                                recentSeasonTopScorers.data.map((player, idx) => (
                                    <li key={idx} className={listItemClass}>
                                        <div className="flex justify-between">
                                            <span>{player.player_name}</span>
                                            <span className="font-semibold">{player.goals} goals</span>
                                        </div>
                                    </li>
                                ))
                                :
                                <li className={listItemClass}>
                                    <div className="flex justify-between">
                                        <span>{recentSeasonTopScorers.data.message}</span>
                                    </div>
                                </li>
                            }

                        </ul>
                    </div>

                    <div>
                        <h2 className={titleClass}>All-Time Most Assists</h2>
                        <ul className="list-disc pl-4">
                            {allTimeAssisters && allTimeAssisters.map((player, idx) => (
                                <li key={idx} className={listItemClass}>
                                    <div className="flex justify-between">
                                        <span>{player.player_name}</span>
                                        <span className="font-semibold">{player.assists} assists</span>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </div>
                    <div>
                        <h2 className={titleClass}>{recentSeasonMostAssists.season.name} Most Assists</h2>
                        <ul className="list-disc pl-4">
                            {/* check to see if data is an array of players */}
                            {/* if data is not array, then there are no data for this season, display error message */}
                            {Array.isArray(recentSeasonMostAssists.data) ?
                                recentSeasonMostAssists.data.map((player, idx) => (
                                    <li key={idx} className={listItemClass}>
                                        <div className="flex justify-between">
                                            <span>{player.player_name}</span>
                                            <span className="font-semibold">{player.assists} assists</span>
                                        </div>
                                    </li>
                                ))
                                :
                                <li className={listItemClass}>
                                    <div className="flex justify-between">
                                        <span>{recentSeasonMostAssists.data.message}</span>
                                    </div>
                                </li>
                            }

                        </ul>
                    </div>
                </div>
            )}
        </>
    );

}
