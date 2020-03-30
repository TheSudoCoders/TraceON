import React from 'react';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';

export default function NavDrawer(props) {
  const {
    isOpen,
    setIsOpen
  } = props;

  return (
    <Drawer
      anchor="left"
      open={isOpen}
      onClose={() => setIsOpen(false)}
    >
      <List>
        <ListItem button key="killnik">
          <ListItemText primary="nikgay" />
        </ListItem>
      </List>
    </Drawer>
  );
}
