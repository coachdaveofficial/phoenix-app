export default function organizeMatchData(data) {
    // Parse the date string into a Date object
    const matchDate = new Date(data.date);

    // Format the date string without converting the time zone to local time
    const options = {
        hour: '2-digit',
        minute: '2-digit',
        timeZone: 'UTC'
    };


    // Extract time and date components
    const matchTime = matchDate.toLocaleTimeString([], options);
    const matchDateString = matchDate.toDateString();

    // Access location and score
    const location = data.venue;
    const goals = data.goals;

    let score;
    let opposingTeam;
    // Ensure the Phoenix score comes first when displaying score
    if (data.home_team.name.startsWith("Phoenix")) {
        // score may not be present if is a future match
        if (data.score) {
            score = `${data.score.home} - ${data.score.away}`;
        }

        opposingTeam = data.away_team;
    } else {
        //  score may not be present if is a future match
        if (data.score) {
            score = `${data.score.away} - ${data.score.home}`;
        }

        opposingTeam = data.home_team;
    }

    // Organized data
    const organizedData = {
        time: matchTime,
        date: matchDateString,
        location,
        score,
        opposingTeam,
        goals
    };

    return organizedData;
}