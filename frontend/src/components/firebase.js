import { initializeApp } from "firebase/app";
import {
    GoogleAuthProvider,
    getAuth,
    signInWithPopup,
    browserLocalPersistence,
    setPersistence
  } from "firebase/auth";

import axios from 'axios'

import {
    getFirestore,
    query,
    getDocs,
    collection,
    where,
    addDoc,
  } from "firebase/firestore";
  
  import {firebaseConfig} from './firebaseCredentials'

// PASTE FIRESTORE CREDENTIALS HERE

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const googleProvider = new GoogleAuthProvider();


const signInWithGoogle = async () => {
    try {
        setPersistence(auth, browserLocalPersistence)
        const res = await signInWithPopup(auth, googleProvider);
        const user = res.user;
        const q = query(collection(db, "users"), where("uid", "==", user.uid));
        const docs = await getDocs(q);
        if (docs.docs.length === 0) {
            await addDoc(collection(db, "users"), {
                uid: user.uid,
                name: user.displayName,
                authProvider: "google",
                email: user.email,
            });
      }
        console.log(user)

        user.getIdToken(/* forceRefresh */ true).then(async function(idToken) {
            console.log(idToken);
            generateWebToken(user);
          }).catch(function(error) {
            // Handle error
          });

        return user;
    } catch (err) {
      console.error(err);
      alert(err.message);
      return null;
    }
  };

  const generateWebToken = async (user) => {
    await axios.post("http://localhost:8000/signup", 
            {
              uid: user.uid,
            }).then((res) => {
              console.log(res)
              localStorage.setItem("racacoonie-auth-token", res["data"])
            })
    
  }

  export {signInWithGoogle}