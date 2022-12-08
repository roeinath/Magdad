import React, {useState} from "react";
import PageNavbar from './PageNavbar.js';
import {fetchApi} from "../stores/apiStore";

const DefaultTemplatePage = ({user}) => {
    const [pages, setPages] = useState({categories: null});
    if (pages.categories == null && user != null) {
        fetchApi("/get_page_list/", user).then(
            (result) => {
                result = result.data;
                setPages(result)
            },
            (error) =>{
                console.error("Got Error: ", error)
            })
    }

    return <PageNavbar categories={pages}/>
};

export default DefaultTemplatePage
