import * as React from 'react';
import Backdrop from '@mui/material/Backdrop';
import Box from '@mui/material/Box';
import Modal from '@mui/material/Modal';
import Fade from '@mui/material/Fade';
import Typography from '@mui/material/Typography';
import RoomIcon from '@mui/icons-material/Room';
import RecipeBlock from './RecipeBlock';
import RecipeCards from './RecipeCards';
import { useNavigate } from 'react-router-dom';

const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

export default function CountryMarker({recipe}) {
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  const navigate = useNavigate();

  return (
    <div>
      <RoomIcon onClick={handleOpen} color="error">Open modal</RoomIcon>
      <Modal
        aria-labelledby="transition-modal-title"
        aria-describedby="transition-modal-description"
        open={open}
        onClose={handleClose}
        closeAfterTransition
        BackdropComponent={Backdrop}
        BackdropProps={{
          timeout: 500,
        }}
      >
        <Fade in={open}>
          <Box sx={style}
          onClick={() => {navigate('/recipe/'+recipe.id);}}
          >
            {recipe?
                <RecipeBlock title={recipe['name']} text={recipe['description']} />:
                "Loading..."
            }
          </Box>
        </Fade>
      </Modal>
    </div>
  );
}