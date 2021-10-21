import React from 'react';
import styled from 'styled-components';
import { Draggable } from 'react-beautiful-dnd';

const Container = styled.div`
  border: 1px solid lightgrey;
  border-radius: 2px;
  padding: 2px;
  margin-bottom: 8px;
  font-size: 20px;
  background-color: ${props => (props.isDragging ? 'lightgreen' : 'white')};
`;

export default function Task(props){
  return (
    <Draggable draggableId={props.task.id} index={props.index}>
      {(provided, snapshot) => (
        <Container
          {...provided.draggableProps}
          {...provided.dragHandleProps}
          ref={provided.innerRef}
          isDragging={snapshot.isDragging}
        >
          {props.task.content + ":" + props.task.amount}
        </Container>
      )}
    </Draggable>
  );
}
