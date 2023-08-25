import React from 'react';
// const defaultLogo = "https://www.seekpng.com/png/detail/28-289657_espn-soccer-team-logo-default.png"
const defaultLogo = "https://static.vecteezy.com/system/resources/thumbnails/005/513/063/small_2x/soccer-ball-outline-icon-illustration-on-white-background-free-vector.jpg"
const imgClass = "rounded-full w-auto h-auto xs:h:10 sm:h-10 md:h-20 lg:h-20 xl:h-20 w-auto xs:w:10 sm:w-10 md:w-20 lg:w-20 xl:w-20"
const teamNameClass = "mb-2 xl:text-2xl lg:text-xl md:text-lg sm:text-md xs:text-sm font-bold tracking-tight text-gray-900 dark:text-white"
export default function CardContent({ isActive, children, phoenixLogo, phoenixTeam, opposingTeam, time, date, location }) {
    return isActive ? (
        <div className="p-4 bg-white dark:bg-gray-800 rounded-lg">

            <div className='flex justify-between'>
                <h5 className={teamNameClass}>{phoenixTeam}</h5>
                <h5 className={teamNameClass}>{opposingTeam}</h5>
            </div>

            <div className='grid grid-cols-3 gap-4 content-between'>
                <img className={imgClass} src={phoenixLogo} alt="Phoenix FC Logo" />
                <p className='text-center'>vs.</p>
                <img className={imgClass} src={defaultLogo} alt="Default Opponent Logo" />
            </div>

            <div className="text-center">
                <p className="font-normal text-gray-700 dark:text-gray-400">time: {time}</p>
                <p className="font-normal text-gray-700 dark:text-gray-400">date: {date}</p>
                <p className="font-normal text-gray-700 dark:text-gray-400">location: {location}</p>
            </div>
            {children}
        </div>
    ) : null;
};

