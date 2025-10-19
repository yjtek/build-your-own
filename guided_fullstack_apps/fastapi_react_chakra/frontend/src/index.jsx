
import React from "react";
import {createRoot} from 'react-dom/client';
import {ChakraProvider} from "@chakra-ui/react"

import Header from './components/Header'
import Todos from './components/Todos'

function App() {
    return (
        <ChakraProvider>
            <Header/>
            <Todos/>
        </ChakraProvider>
    )
}

const container = document.getElementById('root')
const root = createRoot(container)
root.render(<App/>)
