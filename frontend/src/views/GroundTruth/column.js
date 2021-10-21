import React from 'react';
import styled from 'styled-components';
import { Droppable } from 'react-beautiful-dnd';
import Task from './task';

const Container = styled.div`
  margin: 1px;
  border: 1px solid lightgrey;
  border-radius: 2px;
  width: 300px;

  display: flex;
  flex-direction: column;
`;
const Title = styled.h5`
  padding: 1px;
  height: 2px;
`;
const TaskList = styled.div`
  padding: 8px;
  transition: background-color 0.2s ease;
  background-color: ${props => (props.isDraggingOver ? 'skyblue' : 'white')};
  flex-grow: 1;
  min-height: 100px;
`;

export default function Column(props){
  return (
    <div>
      <Title>{props.column.title}</Title>
      <Container>
        {/* <Title>{props.column.title}</Title> */}
        <Droppable droppableId={props.column.id}>
          {(provided, snapshot) => (
            <TaskList
              ref={provided.innerRef}
              {...provided.droppableProps}
              isDraggingOver={snapshot.isDraggingOver}
            >
              {props.tasks.map((task, index) => (
                <Task key={task.id} task={task} index={index} />
              ))}
              {provided.placeholder}
            </TaskList>
          )}
        </Droppable>
      </Container>    
    </div>
    
  );
}
