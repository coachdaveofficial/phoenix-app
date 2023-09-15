import React from 'react';
import { PropagateLoader } from 'react-spinners';

const defaultLogo = "https://static.vecteezy.com/system/resources/thumbnails/005/513/063/small_2x/soccer-ball-outline-icon-illustration-on-white-background-free-vector.jpg"
const imgClass = "rounded-full w-auto h-auto xs:h:10 sm:h-10 md:h-20 lg:h-20 xl:h-20 w-auto xs:w:10 sm:w-10 md:w-20 lg:w-20 xl:w-20 mx-auto"
const teamNameClass = "mb-2 xl:text-2xl lg:text-xl md:text-lg sm:text-md xs:text-sm font-bold tracking-tight text-gray-900 dark:text-white"
const goalClass = "xl:text-sm sm:text-xs xs:text-xs text-center transition-scale duration-300 hover:scale-105 border p-2 m-2 rounded-md shadow-md"
export default function MatchCardContent({ isActive, loading, children, phoenixLogo, phoenixTeam, opposingTeam, time, date, location, score, goals }) {
    let phoenixScore;
    let oppScore;
    if (score) {
        // score looks like: "1 - 1"
        // meaning Phoenix score will be position[0] and opposition will be position[3]
        phoenixScore = score[0]
        oppScore = score[4]
    }


    return isActive && (
        <div className="p-4 bg-white dark:bg-gray-800 rounded-lg">
            {loading ? (
                <div className='grid my-6 justify-center'>
                    <div>
                        <PropagateLoader color="#ff8200" />
                    </div>

                </div>
            ) : (
                <>
                    <div className='flex justify-between'>
                        <h5 className={teamNameClass}>{phoenixTeam}</h5>
                        <h5 className={teamNameClass}>{opposingTeam}</h5>
                    </div>

                    <div className='grid grid-cols-3 gap-4 content-between'>
                        <img className={imgClass} src={phoenixLogo} alt="Phoenix FC Logo" />
                        <p className='text-center'>vs.</p>
                        <img className={imgClass} src={defaultLogo} alt="Default Opponent Logo" />
                    </div>

                    {/* If date is not provided, then do not display any match info */}
                    {
                        date ?
                            <>
                                <ul className='inline-grid grid-cols-1'>
                                    {goals && goals.map((goalObj, idx) => {
                                        return (
                                            <li key={idx} className={goalClass}>
                                                (G) {goalObj.scorer.last_name}, (a) {goalObj.assist.last_name}
                                            </li>
                                        )
                                    })}
                                </ul>

                                <div className="text-center">
                                    <p className="text-2xl font-normal text-gray-700 dark:text-white"><b className='text-orange-400'>{phoenixScore}</b> - {oppScore}</p>
                                    <p className="font-normal text-gray-700 dark:text-white">Time: {time}</p>
                                    <p className="font-normal text-gray-700 dark:text-white">Date: {date}</p>
                                    <p className="font-normal text-gray-700 dark:text-white">Location: {location}</p>
                                </div>
                            </>
                            :
                            <div className='text-center m-2'>
                                <p className="text-2xl font-normal text-gray-700 dark:text-white">
                                    No match info for this team.
                                </p>
                            </div>
                    }
                </>
            )}
        </div>
    );
};

