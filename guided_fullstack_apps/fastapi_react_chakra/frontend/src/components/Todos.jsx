import React, {useState, useEffect, useContext} from 'react';
import {
    Box, Button, Flex, Input, InputGroup, Modal, ModalBody, ModalCloseButton,
    ModalContent, ModalHeader, ModalFooter, ModalOverlay, Stack, Text, useDisclosure
} from "@chakra-ui/react";

const TodosContext = React.createContext({
    todos: [], fetchTodos: () => {}
})

function AddTodo(){
    const [item, setItem] = useState("")
    const {todos, fetchTodos} = useContext(TodosContext)

    const handleInput = event => {
        setItem(event.target.value)
    }

    const handleSubmit = event => {
        const newTodo = {
            "id": todos.length + 1,
            "item": item,
        }
        fetch(
            "http://localhost:8000/todo",
            {
                method: "POST",
                headers: {"Content-Type" : "application/json"},
                body: JSON.stringify(newTodo)
            }
        ).then(fetchTodos)
    }
    return (
        <form onSubmit={handleSubmit}>
            <InputGroup size='md'>
                <Input pr='4.5rem' type='text' placeholder='Add a todo item' aria-label='Add a todo item' onChange={handleInput}>
                </Input>
            </InputGroup>
        
        </form>
    )
}

function UpdateTodo({item, id}){
    const {isOpen, onOpen, onClose} = useDisclosure()
    const [todo, setTodo] = useState()
    const {fetchTodos} = React.useContext(TodosContext)

    const updateToDo = async() => {
        await fetch(
            `http://localhost:8000/todo/${id}`,
            {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({item:todo})
            }
        )
        onClose()
        await fetchTodos()
    }

    return (
        <>
            <Button 
            h='2rem'
            fontSize='1rem'
            fontWeight='bold'
            colorScheme='twitter'
            borderRadius='10px'
            boxShadow='md'
            _hover={{
                bg: 'facebook.500'
            }}
            size='sm'
            onClick={onOpen}
            >
                Update Todo
            </Button>

            <Modal
            isOpen={isOpen}
            onClose={onClose}
            >
                <ModalOverlay>
                    <ModalContent>
                        <ModalHeader>Update Todo</ModalHeader>
                        <ModalCloseButton/>
                        <ModalBody>
                            <InputGroup size='md'>
                                <Input
                                pr='4.5rem'
                                type='text'
                                placeholder='Update todo item'
                                aria-label='Update todo item'
                                value={todo}
                                onChange={e => setTodo(e.target.value)}
                                >
                                
                                </Input>
                            </InputGroup>
                        </ModalBody>
                        <ModalFooter>
                            <Button 
                            h='2rem'
                            fontSize='1rem'
                            fontWight='bold'
                            colorScheme='twitter'
                            borderRadius='10px'
                            boxShadow='md'
                            _hover={{
                                bg: "facebook.500"
                            }}
                            size='sm'
                            onClick={updateToDo}
                            >
                                Update todo
                            </Button>
                        </ModalFooter>
                    </ModalContent>
                </ModalOverlay>
            
            </Modal>
        
        </>
    )
}

function TodoHelper({item, id, fetchTodos}){
    return (
        <Box p={1} shadow='sm'>
            <Flex justify='space-between'>
                <Text mt={4} as='div'>
                    {item}
                    <Flex align='end'>
                        <UpdateTodo item={item} id={id} fetchTodos={fetchTodos}/>
                        <DeleteToDo id={id} fetchTodos={fetchTodos}/>
                    </Flex>
                </Text>
            
            </Flex>
        
        </Box>
    )
}

function DeleteToDo({id}) {
    const {fetchTodos} = React.useContext(TodosContext)
    
    const deleteTodo = async() => {
        await fetch(
            `http://localhost:8000/todo/${id}`,
            {
                method: 'DELETE',
                headers: {"Content-Type": "application/json"},
                body: {"id": id}
            }
        )
        await fetchTodos()
    }
    return (
        <Button
        h='2rem'
        fontSize='1rem'
        fontWeight='bold'
        colorScheme='yellow'
        borderRadius='10px'
        boxShadow='md'
        _hover={{bg: 'red.500'}}
        size='sm'
        onClick={deleteTodo}
        >
            Delete Button
        </Button>
    
    )
}

export default function Todos() {
    const[todos, setTodos] = useState([])
    
    const fetchTodos = async() => {
        const response = await fetch("http://localhost:8000/todo")
        const todosData = await response.json() 
        setTodos(todosData.data)
    }

    useEffect(() => {
        fetchTodos()
    }, [])

    return (
        <TodosContext.Provider value={{todos, fetchTodos}}>
            <AddTodo/>
            <Stack spacing={5}>
                {todos.map((todo) => (
                    // <b>{todo.item}</b>
                    <TodoHelper item={todo.item} id={todo.id} fetchTodos={fetchTodos}></TodoHelper>
                ))}
            </Stack>
        </TodosContext.Provider>
    )
}
