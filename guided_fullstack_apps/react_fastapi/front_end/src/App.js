import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
import {Button} from 'react-bootstrap'
import NavBar from './components/NavBar'
import {BrowserRouter as Router, Link, Route, Switch, Routes} from 'react-router-dom'
import { ProductProvider, ProductContext } from './ProductContext';
import ProductsTable from './components/ProductsTable'
import AddProducts from './components/AddProducts'
import UpdateProduct from './components/UpdateProduct'
import {UpdateProductContextProvider} from './UpdateProductContext'

function App() {
    const [showAddProduct, setShowAddProduct] = useState(false);
    return (
    <div>
        <Router>
        <Routes>
            <UpdateProductContextProvider>
                <Route element={<ProductProvider />}></Route>
                <Route path="/" element={
                <ProductProvider>
                    <NavBar />
                    <div className="container mt-4 mb-4">
                        <div className="row justify-content-center">
                            <div className="col-sm-10 col-xs-12">
                            {/* <Button variant="primary" onClick={() => setShowAddProduct(!showAddProduct)}>
                                {showAddProduct ? "Hide Add Product" : "Add Product"}
                            </Button>
                            {showAddProduct && <AddProducts />} */}
                                <ProductsTable />
                            </div>
                        </div>
                    </div>
                </ProductProvider>
                } />
                <Route exact path="/addproduct" element={<AddProducts/>}/>
                <Route exact path="/updateproduct" element={<UpdateProduct/>}/>
            </UpdateProductContextProvider>
            
        </Routes>
        </Router>
    </div>
    );
}

export default App;