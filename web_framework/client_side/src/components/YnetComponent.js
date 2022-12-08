import React, {useEffect, useState} from "react";
import "./ticker.css";
import {fetchApi} from "../stores/apiStore";
import HebrewLabel from "./HebrewLabel";
import "./ticker.css"
import {Container} from "react-bootstrap";
import {Hidden} from "@material-ui/core";
import MultiComponentRender from "../multiComponentRender/MultiComponentRender";

const Title = () => {
    return (
        <div className="title">
            <h2>מבזקים Ynet</h2>
        </div>
    );
};

const News = (props) => {
    return (
        <div className="news">
            <h2 className="time">{props.time}</h2>
            <h2 className="text">{props.text}</h2>
        </div>
    );
};

const NewsItems = (props) => {
    console.log("news item!", props);
    if (!props.news || !Array.isArray(props.news)) {
        console.log("Error ",props.news, typeof props.news);
        return null;
    }
    return <div className="slide">
        {props.news.map((x, index) => (
            <News key={index} text={x.title} time={x.pubDate}/>
        ))}
    </div>
};

const YnetComponent = (props) => {
    const [news, setNews] = useState({});
    const [isLoading, setIsLoading] = useState(false);
    const [firstFetch, setFirstFetch] = useState(true);
    const [error, setError] = useState(null);

    const load_ynet_data = async () => {
        console.log("fetch ynet");
        fetchApi("/api/get_ynet_news/", props.login).then(
            (result) => {
                setNews(result.data.news);
            },
            (error) => {
                setError(true);
            }
        );
    }

    if (firstFetch) {
        setFirstFetch(false);
        load_ynet_data().then(() => {
            setIsLoading(false);
        });
    }

    // updates the news every 10 minutes ( 10 minutes * 60 seconds * 1000 miliseconds)
    useEffect(() => {
      var interval = setInterval(load_ynet_data, 10 * 60 * 1000);
      return () => clearInterval(interval);
    });

    if (error)
        return (<HebrewLabel color={'red'}>שגיאה בטעינת המידע.</HebrewLabel>);
    else if (isLoading)
        return (<HebrewLabel>טוען מידע...</HebrewLabel>);
    else {
        return (
            <div className="YnetComponent" dir="rtl">
                <Title/>
                <div className="news-container">
                    <NewsItems news={news}/>
                    <NewsItems news={news}/>
                </div>
            </div>
        );
    }
};

export default YnetComponent;