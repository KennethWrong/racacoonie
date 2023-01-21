import * as React from 'react';
import {useState, useEffect} from 'react';
import Button from '@mui/material/Button';
import LoadingButton from '@mui/lab/LoadingButton';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import LogoutIcon from '@mui/icons-material/Logout';
import GoogleIcon from '@mui/icons-material/Google';
import Typewriter from "typewriter-effect";
import {handleSignOut, inMemoryPersistenceLogin, signInWithGoogle} from '../components/firebase'
import { Navigate, useNavigate} from 'react-router-dom'
import {useMemo} from 'react'


function Login() {
    const [loggedin, setLoggedin] = useState(false);
    const [loading, setLoading] = useState(false);
    const [hi, sethi] = useState(false)
    const navigate = useNavigate();

    


    useMemo(() => {
        // storing input name
        var authToken = localStorage.getItem("racacoonie-auth-token");

        
        if (authToken) {
            setLoggedin(true);
        }
        
      }, []);// Navbar and routing on first open


    const handleSignInWithGoogle = async (e) => {
        e.preventDefault();
        setLoading(true);
        var user = await signInWithGoogle();
        if(user) {
            setLoggedin(true);
            setLoading(false);
            return navigate("/")
        }
        
    }
    
    const handleSignOutButton = async (e) => {
        e.preventDefault();
        setLoading(true);
        setTimeout(() => {
            handleSignOut();
            setLoggedin(false);
            setLoading(false);
        }, 1000);
    }

    return (
        <Grid
            container
            spacing={0}
            direction="row"
            alignItems="center"
            justifyContent="space-around"
            style={{ minHeight: '100vh' }}
            >
            <Grid item alignItems="center" justifyContent="center">
                <Box>
                    <Box
                    component="img"
                    sx={{
                    marginLeft:24,
                    height: 350,
                    width: 350,
                    maxHeight: { xs: 250, md: 250 },
                    maxWidth: { xs: 350, md: 250 },
                    }}
                    alt="Icon of racoon"
                    src="https://cdn-icons-png.flaticon.com/512/235/235394.png"
                    />
                </Box>
                <h1
                    className="text-8xl font-bold tracking-wider text-blue-800
                                transition duration-500 ease-in-out hover:text-red-800 transform hover:-translate-y-1 hover:scale-110 ..."
                >RACACOONIE
                </h1>
                <div className="text-5xl font-bold tracking-wider text-blue-800 m-7
                                transition duration-500 ease-in-out hover:text-red-800 transform hover:-translate-y-1 hover:scale-110 ...">
                    <Typewriter
                    options={{
                        autoStart: true,
                        loop: true,
                        }}
                    onInit={(typewriter)=> {
                    
                    typewriter
                        
                    .typeString("LET 'EM COOK!")
                        
                    .pauseFor(1000)
                    .deleteAll()
                    .start();
                    }}
                    />
                </div>
            </Grid>
            <Grid item xs={3}>
                    <LoadingButton
                    size="large"
                    onClick={handleSignInWithGoogle}
                    endIcon={<GoogleIcon />}
                    loading={loading}
                    loadingPosition="end"
                    variant="contained"
                  >
                    <span>Log In With Google</span>
                  </LoadingButton>
            </Grid>   
            
        </Grid> 
    )
}

export default Login