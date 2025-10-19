import React from 'react'
import react, {useEffect, useContext} from 'react'
import { Table } from 'react-bootstrap';  // Import the Table component from react-bootstrap
import {ProductContext} from "../ProductContext"
import ProductRow from "./ProductsRow"
import {useNavigate} from 'react-router-dom'
import {UpdateProductContextProvider} from '../UpdateProductContext'


const ProductsTable = () => {
    const [products, setProducts] = useContext(ProductContext)
    const [updateProductInfo, setUpdateProductInfo] = useContext(UpdateProductContextProvider)

    let navigate = useNavigate()

    const handleDelete = (id) => {
        fetch("http://127.0.0.1:8000/product/" + id, {
            method: "DELETE",
            headers: {
                accept: 'application/json'
            }
        })
        .then(resp => {
            return resp.json()
        })
        .then(result => {
            if(result.status === 'ok'){
                const filteredProducts = products.data.filter((product) => product.id !== id)
                setProducts({data: [...filteredProducts]})
                alert("Product deleted")
            } else {
                alert('Product deletion failed')
            }
        })
            
    }

    const handleUpdate = (id) => {
        console.log('Hello!')
        const product = products.data.filter(product => product.id === id)[0]
        setUpdateProductInfo({
            ProductName: product.name,
            QuantityInStock: product.quantity_in_stock,
            QuantitySold: product.quantity_sold,
            UnitPrice: product.unit_price,
            Revenue: product.revenue,
            ProductId: id
        })

        navigate("/updateproduct")
    }

    useEffect(() => {
        const fetchProducts = async() => {
            try {
                const response = await fetch("http://127.0.0.1:8000/product");
                if (!response.ok) {
                throw new Error('Network response was not ok');
                }
                const results = await response.json();
                console.log(results);
                setProducts({ "data": [...results.data] });
            } catch (error) {
                console.error('Failed to fetch products:', error);
            }
        };

        fetchProducts();

        // fetch("http://127.0.0.1:8000/product")
        // .then(resp => {
        //     return resp.json();
        // }).then(results => {
        //     console.log(results)
        //     setProducts({"data": [...results.data]})
        // })
    }, [setProducts])

    return (
    <div>
        <Table striped bordered hover>
            <thead>
                <tr>
                    <th>Id</th>
                    <th>Product Name</th>
                    <th>Quantity In Stock</th>
                    <th>Quantity Sold</th>
                    <th>Unit Price</th>
                    <th>Revenue</th>
                    <th>Actions</th>
                </tr>
            </thead>
            {/* <tbody>
                {products.data.map(product => (
                    <ProductRow
                        id={product.id}
                        name={product.name}
                        quantity_in_stock={product.quantity_in_stock}
                        quantity_sold={product.quantity_sold}
                        unit_price={product.unit_price}
                        revenue={product.revenue}
                        key={product.id}
                    />
                ))}
            </tbody> */}
            <tbody>
            {products.data && products.data.length > 0 ? (
                products.data.map((product) => (
                <ProductRow
                    key={product.id}
                    id={product.id}
                    name={product.name}
                    quantity_in_stock={product.quantity_in_stock}
                    quantity_sold={product.quantity_sold}
                    unit_price={product.unit_price}
                    revenue={product.revenue}
                    handleDelete = {handleDelete}
                    handleUpdate = {handleUpdate}
                />
                ))
            ) : (
                <tr>
                <td colSpan="7">No products available</td>
                </tr>
            )}
            </tbody>
        </Table>
    </div>
    )
}

export default ProductsTable