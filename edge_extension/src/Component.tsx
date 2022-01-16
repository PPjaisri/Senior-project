import { useState, useEffect } from 'react';
import {
  Tabs, Tab,
  InputGroup,
  FormControl,
  Button,
  Badge
} from 'react-bootstrap';
import './Component.css';
import './Barloader.css';
import { useNavigate, useLocation } from 'react-router-dom';
import { sendLink } from './Service';

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

  function click() {
    passLink('link', link);
  };

  async function passLink(type: string, data: string) {
    const passLink = {
      message_type: 'link',
      message: link
    };

    let res = await sendLink(passLink);
    if (res) {
      navigate('/load', { state: res });
    } else {
      console.log('failed');
    };
  };

  function onKeyPress(code: string) {
    if (code === 'Enter') {
      passLink('link', link);
    } else if (code === 'NumpadEnter') {
      passLink('link', link);
    }
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
          onKeyPress={(event: any) => onKeyPress(event.code)}
        />
      </InputGroup>
      <Button
        variant="primary"
        id="content_submit"
        onClick={click}
      >
        Search
      </Button>
    </div>
  );
};

function ContentSearch() {
  const [content, getContent] = useState('');
  let navigate = useNavigate();

  async function passContent() {
    const passContent = {
      message_type: 'content',
      message: content
    };
    
    let res = await sendLink(passContent);
    if (res) {
      navigate('/load', { state: res });
    } else {
      console.log('failed');
    };
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
        variant="primary"
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
    const data = {
      type: 'image',
      data: image
    };
    navigate('/load', { state: data });
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
      </InputGroup>
      <Button
        variant="primary"
        id="content_submit"
        onClick={passImage}
      >
        Search
      </Button>
    </div>
  );
}

function Starter() {
  return (
    <div>
      <br />
      <h4 className='text-center'>
        <strong>
          --- Thai news matcher ---
        </strong>
      </h4>
    </div>
  );
};

function BarLoader() {
  let { state }: any = useLocation();
  let navigate = useNavigate();

  function loading() {
    setTimeout(() => {
      navigate('/result', {
        state: {
          type: state.message_type,
          search: state.message,
          result: state.result
        }
      });
    }, 2000);
  };

  useEffect(() => {
    loading()
  }, []);

  return (
    <div className="spinner-container">
      <svg
        width="87"
        height="50"
        viewBox="0 0 87 50"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <g id="loader_bars">
          <g id="upperbar">
            <rect
              id="1_2"
              width="67"
              height="14"
              rx="7"
              fill="#FF72C6"
            />
          </g>
          <g id="middlebar">
            <rect
              id="Rectangle 2"
              x="20" y="18"
              width="67"
              height="14"
              rx="7"
              fill="#FF3AB0"
            />
          </g>
          <g id="bottombar">
            <rect
              id="3_2" y="36"
              width="67"
              height="14"
              rx="7"
              fill="#FD0098"
            />
          </g>
        </g>
      </svg>
      <p>Loading</p>
    </div>
  )
}

function ReturnResult(obj: any) {

  const [show, showElement] = useState(false)
  const [buttonName, setButtonName] = useState('Show')

  function showContent() {
    showElement(!show)
    if (buttonName == 'Show') {
      setButtonName('Close')
    } else {
      setButtonName('Show')
    };
  };

  console.log(obj)

  return (
    <div id={obj.obj.index}>
      <hr />
      <div className='jumbotron'>
        <p>
          <span>Link: </span>
          <a href={obj.obj.url} target='_blank'><Badge>CLICK HERE</Badge></a>
        </p>
        <p>{obj.obj.headline}</p>
        <Button
          onClick={showContent}
          className='show_content'
        >
          {buttonName} Content
        </Button>
        {show ? <div>
          <br />
          <p>{obj.obj.content}</p>
        </div> : null}
      </div>
    </div>
  );
}

export {
  SearchBar,
  Starter,
  BarLoader,
  ReturnResult
};