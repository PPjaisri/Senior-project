import { useState, useEffect } from 'react';
import {
  Tabs, Tab,
  InputGroup,
  FormControl,
  Button,
  Badge,
  Container
} from 'react-bootstrap';
import './Component.css';
import './Barloader.css';
import { Messaging } from 'react-cssfx-loading';
import { useNavigate, useLocation, Navigate } from 'react-router-dom';
import { sendImage, sendLink } from './services/Service';
import config from './services/config';
import 'facebook-js-sdk';
import { fb_response } from './types';

function SearchBar() {
  const [authResponse, setAuthResponse] = useState<fb_response | undefined>(undefined)

  window.fbAsyncInit = function () {
    FB.init({
      appId: config.CLIENT_ID_FB,
      cookie: true,
      xfbml: true,
      version: '12.0'
    });

    FB.AppEvents.logPageView();

  };

  function getStatus() {
    FB.getLoginStatus(function (response: any) {
      setAuthResponse(response)
    });

    if (authResponse?.status === 'connected') {
      localStorage.setItem('FB_Access_token', authResponse.authResponse.accessToken)
    }
  }
  // console.log(authResponse?.authResponse);

  function RenderElement() {
    if (authResponse?.status === 'connected') {
      return (
        <div>
          <LinkSearch />
          <FacebookLogin />
        </div>
      );
    } else {
      return (
        <FacebookLogin />
      );
    }
  }

  useEffect(() => {
    getStatus()
  }, []);

  return (
    <Tabs
      defaultActiveKey="link"
      transition={true}
      className="mb-3"
    >
      <Tab eventKey="link" title="Link">
        <RenderElement />
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

function FacebookLogin() {
  function FB_login() {
    FB.login(function (response) {
      console.log(response)
    });
  };

  return (
    <Container className='text-center'>
      <div id="fb-root" />
      <div
        className="fb-login-button"
        data-width="" data-size="large"
        data-button-type="login_with"
        data-layout="rounded"
        data-auto-logout-link="true"
        data-use-continue-as="true"
        onClick={FB_login}
      />
    </Container>
  );
};

function LinkSearch() {
  const [link, getLink] = useState('');
  const [status, getStatus] = useState('')
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
      <label>Paste facebook link here</label>
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
  const [image, getImage] = useState<any>([] || {} || '');
  const [image_link, getImageLink] = useState('');
  let imageData = new FormData();

  let navigate = useNavigate();

  function onKeyPress(code: string) {
    if (code === 'Enter') {
      passImage();
    } else if (code === 'NumpadEnter') {
      passImage();
    }
  };

  async function passImage() {
    imageData.append('image', image, image.name)
    imageData.append('text', 'hello')
    console.log(imageData)
    const passImage = {
      message_type: 'image',
      message: imageData
    };

    let res = await sendImage(imageData);
    if (res) {
      // navigate('/load', { state: res });
    } else {
      console.log('failed');
    };
    // navigate('/load', { state: passImage });
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
          onChange={(event: any) => {
            getImage(event.target.files[0])
          }}
        />
      </InputGroup>
      <label>or, Enter the image URL</label>
      <p />
      <InputGroup className="mb-3">
        <FormControl
          placeholder="Paste link here"
          aria-label="News link"
          onChange={(event: any) => getImageLink(event.target.value)}
          onKeyPress={(event: any) => onKeyPress(event.code)}
        />
      </InputGroup>
      <Button
        variant="primary"
        id="content_submit"
        // onClick={abc}
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
    <div
      className="spinner-container"
    >

      <Messaging />
      {/* <svg
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
      <p>Loading</p> */}
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