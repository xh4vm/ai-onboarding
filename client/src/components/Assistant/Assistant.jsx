import React, { useEffect, useRef, useState } from 'react';
import salut from "../../assets/salut.svg";
import sendIcon from "../../assets/send.svg";
import axios from 'axios';
import './Assistant.scss';
import {json} from "react-router-dom";

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

const Assistant = () => {
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [messages, setMessages] = useState([


]);
    const [newMessage, setNewMessage] = useState('');
    const [gigachatResponse, setGigachatResponse] = useState(null);

    const dialogRef = useRef(null);

    useEffect(() => {
        const handleOutsideClick = (event) => {
            if (dialogRef.current && !dialogRef.current.contains(event.target)) {
                setIsDialogOpen(false);
            }
        };

        document.addEventListener('click', handleOutsideClick);

        return () => {
            document.removeEventListener('click', handleOutsideClick);
        };
    }, []);

    const handleAssistantClick = (event) => {
        event.stopPropagation();
        setIsDialogOpen(!isDialogOpen);
    };

    const responseGigachat = async (usrMessage) => {
        const token =
            "eyJjdHkiOiJqd3QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiUlNBLU9BRVAtMjU2In0.Ec6AKsX97ODLpm8cttqftDQM_8HBGXqTbHXPzhx3SneF7Fqa1wN2ram1nV9zdBefvSE1LLLT-b2-CDjmw7D2GF8eH9QEO9_2LV0cjPRsqaAapF-STdPXO1LiMdWrUIKhzUVdYerWbmgdScPyrOPWa7Fdq-Sbg4sgY598kXMcoymwDYd5DQO-BHXyXWc5pjJs1XKET7HvxkGetL7fGk6GUj73Ds-x8isQVHh1LRd-VklBDm1uIEbmqdzjzozPv-YOE92bRiKEqkOfpOnskDtuWyfTLeHcEejsid27mpcEciSmO5Yf_xbZFR1mnkjJyEj7PzUTk1Ym2UyzFv81jbSNVw.iFIPFqeGoitnjRnBfKh4_A.BhNd3Os5z1KIB1mKlXmIsVgroEgFNfBUAubL7TX4wghX834v_l2iar02cML_eVvl0OjvuUQ8eLZSiT_dlUHMaRPJTVEuCKVz_OTBPWO1ovLw15HbIVH_Dr5A3UHSqVlNmATn70Z4I4Jo0Lm9hTDjeEGG7FPjqzzTb2gXHFQnCpPFtk0SIz819Fxmku2BKUMb6OJcdmJwn4T0z2WWFYsgXDEZLBRsfav_9rbFYGu0TQz9Pp6nK2fEai0jRxATZNVD9vTB3QDnt8I642IrWl3ZzHFuSWiEWe1fy4fKa7eZwoyzZiaelodZHo-cO_4bTrr929lMcMlMC0e72mB4w_rp_2QRQKG7t9ANYgTZk6_-rl0KQy-uIytKOPsAA_kgT7jmHMJEiQlTbjUzcAExdsHYrp7DOOCd5VI1FHJoTfh1J2qAJK87l_MJISY5LPDA_CgTlUmtmMS_czC2xExvDfZIdryFNsUzLXjieQ6zzT0-bXpG1di9FdP3S8Zf7YkxXO5EilrDCMOCHAJvNuInjwVI80CSTF8aSTKMALVKfIML_FhPIuimoyyMOsnGU6nA9AlMmVThZtm5JMbHU7Bkw8G2fbj7FbXub7r7Ba8TzczqMG3_VZfhnxE6Dg4s4sx7o8aFuaD4AlmXUf8I81_2MBQpeTSeODnZJelKgSUqAH-v1MmxQzVd5xYSI2cSnPE93I5AZDvgjdRRU0Pv8N6NHQ0wDXGJ9Z2txXELyZMfHFTZweI.4SAG7NTRF9HQ40-kwSJzHrcLNZgZLybseSY5lrBCc0E";
        const userMessage = usrMessage;
        const systemMessage = "Тебя зовут Кирилл, и ты ассистент Андеррайтера при проверке документов и одобрении кредита. Если в конце собщения стоит ВАЖНО, значит ответ надо дать в любом случае, с учётом имеющейся информации и факторов";

        const url = "http://51.250.111.118/onboarding/api/v1/chat";
        const headers = {
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, PUT, POST, DELETE, PATCH, OPTIONS",
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            "X-Request-Id": "c575148e-8ee4-4a77-98b1-b4b7b58233f4",
            "X-Session-Id": "ee7853ed-9b3e-45e6-a2ee-d2fce1a06c55",
            "Allow": "GET, POST",
            "X-Frame-Options": "SAMEORIGIN",
            "X-XSS-Protection": "1; mode=block",
            "X-Content-Type-Options": "nosniff",
        };

        const data = {
            token: token,
            user: userMessage,
            system: systemMessage,
        };

        try {
            const response = await axios.post(url, data, { headers: headers });

            if (response.status === 200) {
                setGigachatResponse(response['data']);
                setMessages([
                    ...messages,
                    { text: userMessage, sender: 'user' },
                    { text: response['data'], sender: 'system' },
                ]);
            } else {
                console.error("Error: ", response.status);
            }
        } catch (error) {
            console.error("Error fetching response from Gigachat API", error);
        }
    };

    const sendMessage = async (message) => {
        message = newMessage
        setNewMessage("")
        console.log(message)
        const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiZGJlMTVkOC1jYzQyLTRjNzMtYTA3ZC0yZjdjNDFjOWQ0YzMiLCJleHAiOjE3MDE2NDAyMzguMjIwNTIxLCJqdGkiOiJiNGZlODEyZC1jZDIxLTRhY2ItOTkwOC05YmIwNWFmZTQ0NTgiLCJlbWFpbCI6InRlc3RAbWFpbC5ydSJ9.vTDTYpnVC33uFZ_6B5pMThxK0-vkQpGacUw-xYqSM38"
        const apiUrl = 'http://51.250.111.118/onboarding/api/v1/chat';

        try {
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    "Accept": "*/*",
                    "Access-Control-Allow-Credentials": "true",
                    "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept, Authorization",
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, PUT, POST, DELETE, PATCH, OPTIONS",
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                    "Allow": "GET, POST",
                    "X-Frame-Options": "SAMEORIGIN",
                    "X-XSS-Protection": "1; mode=block",
                    "X-Content-Type-Options": "nosniff",
                },
                body: JSON.stringify({
                    message: message,
                }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }


            const jsonResponse = await response.json();
            console.log('Response:', jsonResponse["answer"]['message']);
            setMessages([
                ...messages,
                { text: message, sender: 'user' },
                { text: jsonResponse["answer"]['message'], sender: 'system' },
            ]);
        } catch (error) {
            console.error('Error:', error.message);
        }
    };

    const handleInputChange = (event) => {
        setNewMessage(event.target.value);
    };

    const handleSendMessage = () => {
        if (newMessage.trim() !== '') {
            responseGigachat(newMessage);
            setNewMessage('');
        }
    };

    return (
        <div className={`assistant ${isDialogOpen ? 'open' : ''}`}>
            {isDialogOpen && (
                <div className="test">
                <div className="dialog-box" ref={dialogRef}>
                    <div className="greeting">Кирилл</div>
                    <div className="message-container">
                        {messages.map((message, index) => (
                            <div key={index} className={`message ${message.sender}`}>
                                {message.text}
                            </div>
                        ))}
                    </div>
                    <div className="inputs">
                        <input
                            type="text"
                            className="search-bar"
                            placeholder="Введите сообщение"
                            value={newMessage}
                            onChange={handleInputChange}
                        />
                        <img src={sendIcon} alt="Send" className="send-icon" onClick={sendMessage} />
                    </div>
                </div>
                </div>
            )}
            <div onClick={handleAssistantClick} className="assistant-logo">
                <img height={70} width={70} src={salut} alt="Salut" />
            </div>
        </div>
    );
};

export default Assistant;
