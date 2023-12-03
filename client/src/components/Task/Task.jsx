import React, { useMemo } from 'react';
import './Task.scss';

const Task = ({ name, time, status }) => {
    const statusText = useMemo(() => {
        if (status === '0') {
            return 'Выполнено';
        } else if (status === '1') {
            return 'В работе';
        } else if (status === '2') {
            return 'На проверке';
        } else {
            return 'Черновик';
        }
    }, [status]);

    const statusColor = useMemo(() => {
        if (status === '0') {
            return 'green';
        } else if (status === '1') {
            return 'blue';
        } else if (status === '2') {
            return 'orange';
        } else {
            return 'gray';
        }
    }, [status]);

    return (
        <div className="taskCard">
            <div className="taskGrid">
                <div className="taskName">
                    <strong>{name}</strong>
                </div>
                <div className="taskTime">
                    <strong>{time}</strong>
                </div>
                <div className="statusCircle" style={{ backgroundColor: statusColor }} />
                <div className="taskStatus">
                    <strong>{statusText}</strong>
                </div>
            </div>
        </div>
    );
};

export default Task;
