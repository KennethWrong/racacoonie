import Button from '@mui/material/Button';
import * as React from 'react';
import {useState} from 'react';
import {signInWithGoogle} from '../components/firebase'


function Login() {

    return (
        <div>
            <Button
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
                onClick={signInWithGoogle}
            >
                Log In With Google
            </Button>
        </div>
    )
}

export default Login