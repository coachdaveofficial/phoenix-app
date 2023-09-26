export default function organizeMatchData(data) {

    // data can be null if there is no match data being passed
    // for example, if there is no upcoming match data available for a specific team
    if (!data) {
        return undefined
    }

    const matchDate = new Date(data.date);

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

    let score = undefined;
    let opposingTeam;
    // Ensure the Phoenix score comes first when displaying score
    if (data.home_team.name.startsWith("Phoenix")) {
        // score may not be present if is a future match
        if (data.score && data.score !== 'vs') {
            score = `${data.score.home} - ${data.score.away}`;
        }

        opposingTeam = data.away_team;
    } else {
        //  score may not be present if is a future match
        if (data.score && data.score !== 'vs') {
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