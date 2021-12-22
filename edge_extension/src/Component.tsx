import { render } from '@testing-library/react';
import { useEffect, useState } from 'react';
import {
  Tabs,
  Tab,
  InputGroup,
  FormControl,
  Button,
  Spinner
} from 'react-bootstrap';
import './Component.css';
import './Barloader.css';
import { useNavigate, useLocation } from 'react-router-dom';

function SearchBar() {
  return (
    <Tabs
      defaultActiveKey="link"
      transition={true}
      className="mb-3"
    >
      <Tab eventKey="link" title="Link">
        <LinkSearch />
      </Tab>
      <Tab eventKey="content" title="Content">
        <ContentSearch />
      </Tab>
      <Tab eventKey="image" title="Image">
        <ImageSearch />
      </Tab>
    </Tabs>
  );
};

function LinkSearch() {
  const [link, getLink] = useState('');
  let navigate = useNavigate();

  function passLink() {
    // sessionStorage.setItem('link', link);
    console.log(link);
    navigate("/load");
  };

  return (
    <div>
      <label>Paste link here</label>
      <p />
      <InputGroup className="mb-3">
        <FormControl
          placeholder="Paste link here"
          aria-label="News link"
          onChange={(event: any) => getLink(event.target.value)}
        />
        <Button
          variant="outline-primary"
          id="link_submit"
          onClick={passLink}
        >
          Search
        </Button>
      </InputGroup>
    </div>
  );
};

function ContentSearch() {
  const [content, getContent] = useState('');
  let navigate = useNavigate();

  function passContent() {
    // sessionStorage.setItem('content', content);
    console.log(content);
    navigate('/load');
  };

  return (
    <div>
      <label>Paste news content here</label>
      <p />
      <InputGroup>
        <FormControl
          as="textarea"
          aria-label="news content"
          id="content_form"
          placeholder="Paste news content here"
          onChange={(event: any) => getContent(event.target.value)}
        />
      </InputGroup> <br />
      <Button
        variant="outline-secondary"
        id="content_submit"
        onClick={passContent}
      >
        Search
      </Button>
    </div>
  );
}

function ImageSearch() {
  const [image, getImage] = useState('');
  let navigate = useNavigate();

  function passImage() {
    // sessionStorage.setItem('image', image);
    console.log(image);
    navigate('/load');
  };

  return (
    <div>
      <label>Upload file here</label>
      <p />
      <InputGroup className="mb-3">
        <FormControl
          type="file"
          aria-label="news image"
          accept='image/*'
          onChange={(event: any) => getImage(event.target.value)}
        />
        <Button
          variant="outline-secondary"
          id="file_submit"
          onClick={passImage}
        >
          Search
        </Button>
      </InputGroup>
    </div>
  );
}

function Wait() {
  console.log('Wait');
  return (
    <div>
      <Spinner
        animation='border'
        variant='info'
        role='load'
        className='spinner'
      />
    </div>
  )
};

function Starter() {
  return (
    <div>
      <br />
      <h4 className='text-center'>
        <strong>
          --- Thai news matcher ---
        </strong>
      </h4>
      <hr />
    </div>
  );
};

function BarLoader() {

  return (
    <div className="spinner-container">

      <svg width="87" height="50" viewBox="0 0 87 50" fill="none" xmlns="http://www.w3.org/2000/svg">
        <g id="loader_bars">
          <g id="upperbar">
            <rect id="1_2" width="67" height="14" rx="7" fill="#FF72C6" />
          </g>
          <g id="middlebar">
            <rect id="Rectangle 2" x="20" y="18" width="67" height="14" rx="7" fill="#FF3AB0" />
          </g>
          <g id="bottombar">
            <rect id="3_2" y="36" width="67" height="14" rx="7" fill="#FD0098" />
          </g>
        </g>
      </svg>


      <p>Loading</p>
    </div>

  )
}

export {
  SearchBar,
  Wait,
  Starter,
  BarLoader
};