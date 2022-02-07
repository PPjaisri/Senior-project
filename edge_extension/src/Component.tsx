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
  // const [authResponse, setAuthResponse] = useState<fb_response | undefined>(undefined)

  // window.fbAsyncInit = function () {
  //   FB.init({
  //     appId: config.CLIENT_ID_FB,
  //     cookie: true,
  //     xfbml: true,
  //     version: '12.0'
  //   });

  //   FB.AppEvents.logPageView();

  // };

  // function getStatus() {
  //   FB.getLoginStatus(function (response: any) {
  //     setAuthResponse(response)
  //   });

  //   if (authResponse?.status === 'connected') {
  //     localStorage.setItem('FB_Access_token', authResponse.authResponse.accessToken)
  //   }
  // }
  // // console.log(authResponse?.authResponse);

  // function RenderElement() {
  //   if (authResponse?.status === 'connected') {
  //     return (
  //       <div>
  //         <LinkSearch />
  //         <FacebookLogin />
  //       </div>
  //     );
  //   } else {
  //     return (
  //       <FacebookLogin />
  //     );
  //   }
  // }

  // useEffect(() => {
  //   getStatus()
  // }, []);

  return (
    <Tabs
      defaultActiveKey="link"
      transition={true}
      className="mb-3"
    >
      <Tab eventKey="link" title="Link">
        {/* <RenderElement /> */}
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
      passImageData()
  }

  async function passImageSite() {
    const passImageData = {
      message_type: 'image',
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

  async function upLoadLink(data: any) {
    console.log(data);
  }

  async function upLoadContent(data: any) {
    let res = await sendLink(data);
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

  async function upLoadImageSite(data: any) {
    console.log(data);
  }

  function upLoadImage(data: any) {
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
      else if (state.data.message_type === 'image')
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