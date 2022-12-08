import React, {useState} from "react";
import {Container, Row, Col} from "react-bootstrap";
import HebrewLabel from "../components/HebrewLabel";
import TalpixLogo from "./TalpixLogo"
import Carousel from "react-bootstrap/Carousel";
import {COLORS, FONTS} from "../constants";
import {fetchApi} from "../stores/apiStore";
import Button from "../components/Button";

const FrontPage = ({user}) => {
    const items = [
        <Container>
            <TalpixLogo size_type={"page"}/>
            <br/>
        </Container>,
        <Container>
            <TalpixLogo size_type={"page"}/>
            <HebrewLabel size="2.5vw" font={FONTS.GISHA} bold color={COLORS.TALPIOT_CYAN}>אתר TalpiX</HebrewLabel>
            <div style={{height: "3vw"}}/>
        </Container>
    ]
    const [quickAccessPages, setPages] = useState(null);
    if (quickAccessPages == null && user != null) {
            fetchApi("/quick_access_pages/", user).then(
                (result) => {
                    result = result.data && result.data.pages;
                    if (result) {
                        setPages(result);
                    }
                },
                (error) => {
                    console.error("Got Error: ", error)
                })
    }
    return <Container style={{justifyContent: 'center'}}>
        <HebrewLabel size="3.4vw" font="Guttman stam">"כְּמִגְדַּל דָּוִיד צַוָּארֵךְ בָּנוּי לְתַלְפִּיּוֹת,
                {<br/>}אֶלֶף הַמָּגֵן תָּלוּי עָלָיו כֹּל שִׁלְטֵי הַגִּבּוֹרִים"</HebrewLabel>
        <Carousel interval={3000} fade wrap style={{minHeight: '45vh'}}>
            {items.map((item) => (<Carousel.Item>{item}</Carousel.Item>))}
        </Carousel>
        <Container style={{justifyContent: 'right'}}>
            <HebrewLabel font={FONTS.SECULAR_ONE} size="lg">גישה מהירה</HebrewLabel>
            <a href="https://sites.google.com/view/portalpiot/">קישור לפורטל</a>
            <Row dir="rtl" style={{marginTop: '1vh', width: '80%', position: 'relative', left: '10%'}}>
                {quickAccessPages && quickAccessPages.map(page =>
                    <Col>
                        <a href={page.url}>
                            <Button onClick={() => {}} text={`ל${page.name}`} font={FONTS.SECULAR_ONE}/>
                        </a>
                    </Col>
                )}
            </Row>
        </Container>

    </Container>
}

export default FrontPage;