export default function organizeMatchData(data) {
        // Parse the date string into a Date object
    const matchDate = new Date(data.date);
  
    // Extract time and date components
    const matchTime = matchDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: true });
    const matchDateString = matchDate.toDateString();
  
    // Access location and score
    const location = data.venue;
    let score;
    let opposingTeam;
    // Ensure the Phoenix score comes first when displaying score
    if (data.home_team.name.startsWith("Phoenix")) {
        score = `${data.score.home} - ${data.score.away}`;
        opposingTeam = data.away_team;
    } else {
        score = `${data.score.away} - ${data.score.home}`;
        opposingTeam = data.home_team;
    }
    
  
    // Organized data
    const organizedData = {
      time: matchTime,
      date: matchDateString,
      location,
      score,
      opposingTeam
    };
  
    return organizedData;
  }