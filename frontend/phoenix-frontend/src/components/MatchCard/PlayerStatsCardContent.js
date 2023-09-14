import React from 'react';

const titleClass = "text-xl font-semibold mb-4";
const listItemClass = "mb-2 p-2 bg-gray-100 dark:bg-gray-700 rounded-lg";

export default function PlayerStatsCardContent({ isActive, allTimeGoalScorers, allTimeAssisters, recentSeasonTopScorers, recentSeasonMostAssists }) {

    return isActive && (
        <div className="p-4 bg-white dark:bg-gray-800 rounded-lg">
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
            <h2 className={titleClass}>Current Season Most Goals</h2>
            <ul className="list-disc pl-4">
                {recentSeasonTopScorers && recentSeasonTopScorers.map((player, idx) => (
                    <li key={idx} className={listItemClass}>
                        <div className="flex justify-between">
                            <span>{player.player_name}</span>
                            <span className="font-semibold">{player.goals} goals</span>
                        </div>
                    </li>
                ))}
            </ul>

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
            <h2 className={titleClass}>Current Season Most Assists</h2>
            <ul className="list-disc pl-4">
                {recentSeasonMostAssists && recentSeasonMostAssists.map((player, idx) => (
                    <li key={idx} className={listItemClass}>
                        <div className="flex justify-between">
                            <span>{player.player_name}</span>
                            <span className="font-semibold">{player.assists} assists</span>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
}
