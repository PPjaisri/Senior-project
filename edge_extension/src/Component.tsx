import { useState, useEffect } from 'react';
import {
  Tabs, Tab,
  InputGroup,
  FormControl,
  Button,
  Badge,
  Container,
  Card,
  Image
} from 'react-bootstrap';
import './Component.css';
import './Barloader.css';
import 'facebook-js-sdk';
import { Messaging } from 'react-cssfx-loading';
import { useNavigate, useLocation, Navigate } from 'react-router-dom';
import { sendImage, sendLink, sendToken } from './services/Service';
import config from './services/config';
import { send_file, send_image_file, send_text } from './services/types';
import FacebookLogin from 'react-facebook-login';
function SearchBar() {
  const [login, setLogin] = useState<any>(false);
  const [data, setData] = useState<any>({});

  const responseFacebook = async (response: any) => {
    setData(response);

    if (response.accessToken) {
      setLogin(true);

      const tokenData = {
        'message_type': 'token',
        'facebook_access_token': response.accessToken
      }
      console.log(response.accessToken);

      const res = await sendToken(tokenData);
      if (res.result === 200)
        console.log('OK');
      else
        console.log('error');
    } else {
      setLogin(false);
    }
  }

  const custom_button = <div className="facebook_button" />

  return (
    <Tabs
      defaultActiveKey="link"
      transition={true}
      className="mb-3"
    >
      <Tab eventKey="link" title="Link">
        {!login &&
          <FacebookLogin
            appId="1009901223209735"
            autoLoad={true}
            fields="name,email,picture"
            scope="public_profile"
            callback={responseFacebook}
            icon={custom_button}
          />
        }
        {
          login &&
          <LinkSearch />
        }
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
  const [status, getStatus] = useState('')
  let navigate = useNavigate();

  function click() {
    passLink();
  };

  function onKeyPress(code: string) {
    if (code === 'Enter') {
      passLink();
    } else if (code === 'NumpadEnter') {
      passLink();
    }
  };

  async function passLink() {
    if (link !== '') {
      const passLink = {
        message_type: 'link',
        message: link
      };

      navigate('/load', {
        state: {
          type: 'string',
          data: passLink
        }
      });
    }
    else
      console.log('error');
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
    if (content !== '') {
      const passContent = {
        message_type: 'content',
        message: content
      };

      navigate('/load', {
        state: {
          type: 'string',
          data: passContent
        }
      });
    }
    else
      console.log('error')
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
      passImageSite();
    } else if (code === 'NumpadEnter') {
      passImageSite();
    }
  };

  function passer() {
    if (image.length == 0)
      if (image_link === '')
        console.log('error')
      else
        passImageSite()
    else
      passImage()
  }

  async function passImageSite() {
    imageData.append('message_type', 'image')
    imageData.append('image', image)
    const passImageData = {
      message_type: 'image_url',
      message: image_link
    };

    navigate('/load', {
      state: {
        type: 'string',
        data: passImageData
      }
    });
  }

  async function passImage() {
    imageData.append('message_type', 'image')
    imageData.append('image', image)
    const passImageData = {
      message_type: 'image',
      message: imageData
    };

    navigate('/load', {
      state: {
        type: 'file',
        data: passImageData
      }
    });
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
        onClick={passer}
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

function Loader() {
  let { state }: any = useLocation();
  let navigate = useNavigate();

  async function upLoadLink(data: send_text) {
    console.log(data);
  }

  async function upLoadContent(data: send_text) {
    const res = await sendLink(data);
    if (res) {
      navigate('/result', {
        state: {
          type: res.message_type,
          search: res.message,
          result: res.result
        }
      });
    } else {
      console.log('failed');
    };
  }

  async function upLoadImageSite(data: send_text) {
    // console.log(data.message);
    const res = await sendLink(data);
    if (res) {
      navigate('/result', {
        state: {
          type: res.message_type,
          search: res.message,
          result: res.result
        }
      });
    }
    else
      console.log('error');
  }

  function upLoadImage(data: send_image_file) {
    console.log('component: ', data.message)
    sendImage(data.message)
      .then((res: any) => {
        navigate('/result', {
          state: {
            type: res.data.message_type,
            search: res.data.message,
            result: res.data.result
          }
        });
      })
  };

  function loading() {
    if (state.type === 'string') {
      if (state.data.message_type === 'link')
        upLoadLink(state.data)
      else if (state.data.message_type === 'content')
        upLoadContent(state.data)
      else if (state.data.message_type === 'image_url')
        upLoadImageSite(state.data)
    }
    else if (state.type === 'file')
      upLoadImage(state.data);
  };

  useEffect(() => {
    loading()
  }, []);

  return (
    <div
      // className="spinner-container"
      className="centered"
    >
      <Messaging />
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
          size='sm'
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
  Loader,
  ReturnResult
};