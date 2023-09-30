"use client"
import React, { useState, useEffect } from 'react';
import ScrollSectionCards from '@/components/scrollSections/ScrollSectionCards';
import ScrollSectionAbout from '@/components/scrollSections/ScrollSectionAbout';
import NavBarFunc from '@/components/navbar/Navbar';
import MatchCard from '@/components/matchCard/MatchCard';
import About from '@/components/about/About';
import LoginForm from '@/components/auth/LoginForm';
import login from '@/helpers/login'
import ScriptForm from '@/components/forms/ScriptForm';
import Modal from '@/components/common/Modal';
import axios from "axios";
import organizeMatchData from '@/helpers/organizeMatchData';
import { RiseLoader } from 'react-spinners';


const API_BASE_URL = 'http://127.0.0.1:8080/api'


export default function Homepage() {
  const [showModal, setShowModal] = useState(false);
  const [refresh, setRefresh] = useState(false);
  const [openStats, setOpenStats] = useState(null);
  const [overThirtyStats, setOverThirtyStats] = useState(null);
  const [overFortyStats, setOverFortyStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const handleModalShow = () => {
    setShowModal(!showModal);
  }
  const handleRefresh = () => {
    setRefresh(!refresh);
  }
  useEffect(() => {

    // Add an event listener for the ESC key press
    document.addEventListener('keydown', (e) => {
      if (showModal && e.key === 'Escape') {
        handleModalShow();
      }
    });

    // Remove the event listener when the component unmounts
    return () => {
      document.removeEventListener('keydown', handleModalShow);
    };
  }, [showModal]);

  useEffect(() => {
    async function getTeamStats() {
      try {
        const result = await axios.get(`${API_BASE_URL}/teams/stats/`);
        setOpenStats(
          {
            prevData: organizeMatchData(result.data.openStats.prev_match),
            upcomingData: organizeMatchData(result.data.openStats.upcoming_match),
            mostGoalsAndAssistsData: {
              mostGoals: result.data.openStats.most_goals,
              mostAssists: result.data.openStats.most_assists
            },
            recentSeasonRecords: {
              mostGoals: result.data.openStats.recent_goals,
              mostAssists: result.data.openStats.recent_assists,
              season: result.data.openStats.recent_season
            }
          }
        );
        setOverThirtyStats(
          {
            prevData: organizeMatchData(result.data.overThirtyStats.prev_match),
            upcomingData: organizeMatchData(result.data.overThirtyStats.upcoming_match),
            mostGoalsAndAssistsData: {
              mostGoals: result.data.overThirtyStats.most_goals,
              mostAssists: result.data.overThirtyStats.most_assists
            },
            recentSeasonRecords: {
              mostGoals: result.data.overThirtyStats.recent_goals,
              mostAssists: result.data.overThirtyStats.recent_assists,
              season: result.data.overThirtyStats.recent_season
            }
          }
        );
        setOverFortyStats(
          {
            prevData: organizeMatchData(result.data.overFortyStats.prev_match),
            upcomingData: organizeMatchData(result.data.overFortyStats.upcoming_match),
            mostGoalsAndAssistsData: {
              mostGoals: result.data.overFortyStats.most_goals,
              mostAssists: result.data.overFortyStats.most_assists
            },
            recentSeasonRecords: {
              mostGoals: result.data.overFortyStats.recent_goals,
              mostAssists: result.data.overFortyStats.recent_assists,
              season: result.data.overFortyStats.recent_season
            }
          }
        );

        setLoading(false);
      } catch (e) {
        console.error('Error fetching team stats:', e);
      }

    }
    getTeamStats();
  }, [refresh]);

  return (
    <>
      <NavBarFunc handleModalShow={handleModalShow} />
      {showModal && <Modal title={"Upload worksheet data"} handleModalShow={handleModalShow}>
        <ScriptForm handleRefresh={handleRefresh} />
      </Modal>
      }

      <ScrollSectionCards sectionId={'section-one'} bgColor={"blue"}>
        {loading ? (
          <>
            <div>
              {/* Empty div to push loader to the center */}
            </div>
            <div className="flex justify-center items-center h-96">
              <div className='justify-center'>
                <RiseLoader color="#ff8200" />
              </div>
            </div>
            <div>
              {/* Empty div to push loader to the center */}
            </div>
          </>

        ) :
         (
          <>
            <MatchCard phoenixTeam={"Open"} teamData={openStats} />
            <MatchCard phoenixTeam={"O30"} teamData={overThirtyStats} />
            <MatchCard phoenixTeam={"O40"} teamData={overFortyStats} />
          </>
        )}
      </ScrollSectionCards>
      <ScrollSectionAbout sectionId={'section-two'} bgColor={"orange"} >
        <About
          youtubeLink={"https://www.youtube.com/@Phoenix_FC/featured"}
          instagramLink={"https://www.instagram.com/phoenix_fc_pdx/"}
          facebookLink={"https://www.facebook.com/Phoenixfc.pdx"}
          leagueLink={"http://gpsdsoccer.com/"}
          OASALink={"https://www.oregonadultsoccer.com/"}
          indoorLink={"https://pdxindoorsoccer.com/"}
        />
      </ScrollSectionAbout>

    </>
  )
}
