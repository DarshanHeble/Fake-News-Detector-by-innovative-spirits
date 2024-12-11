import React from 'react'
import style from './Header.module.css'
import GroupImg from '../../assets/Group.png'

export const Header = () => {
  return (
    <div className={style.header}>
        <div className={style.logocon}>
            <svg className={style.logosvg} width="167" height="195" viewBox="0 0 167 195" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M84 50L62.3494 37.5L62.3494 12.5L84 1.62913e-06L105.651 12.5L105.651 37.5L84 50Z" fill="black"/>
            <path d="M43.7858 75.7877L22.0795 88.1909L0.484937 75.5944L0.596567 50.5946L22.3028 38.1914L43.8974 50.788L43.7858 75.7877Z" fill="black"/>
            <path d="M122.544 75.713L122.493 50.7131L144.118 38.1692L165.794 50.6252L165.845 75.6251L144.22 88.1691L122.544 75.713Z" fill="black"/>
            <path d="M43.8561 146.04L22.454 158.96L0.563088 146.886L0.0743392 121.891L21.4765 108.97L43.3673 121.044L43.8561 146.04Z" fill="black"/>
            <path d="M123.395 120.711L144.985 108.106L166.696 120.501L166.817 145.501L145.227 158.106L123.516 145.711L123.395 120.711Z" fill="black"/>
            <path d="M83.9999 67.0549L110.008 82.0073L110.063 112.007L84.1097 127.055L58.1016 112.102L58.0467 82.1024L83.9999 67.0549Z" fill="black"/>
            <path d="M84.2395 144.12L105.83 156.724L105.71 181.723L83.9997 194.119L62.4093 181.516L62.5291 156.516L84.2395 144.12Z" fill="black"/>
            <path d="M144 63L145 133" stroke="white" stroke-width="3" stroke-linecap="round"/>
            <path d="M84 26L144 63" stroke="white" stroke-width="3" stroke-linecap="round"/>
            <path d="M84 26L22 63" stroke="white" stroke-width="3" stroke-linecap="round"/>
            <path d="M84 169L145 134" stroke="white" stroke-width="3" stroke-linecap="round"/>
            <path d="M84 97L22 63" stroke="white" stroke-width="3" stroke-linecap="round"/>
            <path d="M84 97L143 63" stroke="white" stroke-width="3" stroke-linecap="round"/>
            <path d="M84 97V168" stroke="white" stroke-width="3" stroke-linecap="round"/>
            <path d="M22 63V134" stroke="white" stroke-width="3" stroke-linecap="round"/>
            <path d="M84 169L22 135" stroke="white" stroke-width="3" stroke-linecap="round"/>
            </svg>
            <span className={style.fakenewsStyle}>FAKE NEWS <span className='detectroStyle'>DETECTOR</span></span>
        </div>
        <div className={style.TeamCon}>
            <div className={style.groupBTN}>
                <span className={style.groupBTNfont}>Our Team</span>
                <img className={style.groupImg} src={GroupImg} alt="GI" />
            </div>
        </div>
    </div>
  )
}
