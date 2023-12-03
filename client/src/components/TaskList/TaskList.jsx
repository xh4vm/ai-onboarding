import React from 'react';
import "./TaskList.scss";
import Task from "../Task/Task"

const TaskList = ({tasks}) => {
    return (
        <div className='taskList'>
            <div className="greeting"> <h1>Мои Задачи</h1></div>
            {tasks.map((task, index) => {
                return <Task key={index} name={task.name} time={task.time} status={task.status} />
            })}
        </div>
    );
};

export default TaskList;