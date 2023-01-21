import * as React from 'react';
import {useState, useEffect} from 'react';
import axios from 'axios';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import {inMemoryPersistenceLogin, signInWithGoogle} from '../components/firebase'
import { Navigate } from 'react-router-dom';

function Login() {
    const [loggedin, setLoggedin] = useState(false);

    useEffect(() => {
        // storing input name
        var authToken = localStorage.getItem("racacoonie-auth-token");
        if (authToken) {
            setLoggedin(true);
        }
        
      }, [loggedin]);// Navbar and routing on first open


    const handleSignInWithGoogle = async (e) => {
        e.preventDefault();

        var user = await signInWithGoogle();
        if(user) {
            setLoggedin(true);
        }
        
    }

    return (
        <Container maxWidth="md">
            <h3>RACACOONIE</h3>
            {!loggedin ?
                <Button
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
                onClick={handleSignInWithGoogle}
            >
                Log In With Google
            </Button> :

            <Navigate to="/" replace />
            }
        </Container>
    )
}

export default Login