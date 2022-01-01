import {
  RouteObject,
  useRoutes,
  useNavigate,
  useLocation
} from 'react-router-dom';
import {
  Button,
  Container,
  Badge
} from 'react-bootstrap';
import { Starter, SearchBar, BarLoader } from './Component'
import './App.css';
import { useState } from 'react'

function App() {

  let routes: RouteObject[] = [
    {
      path: "/",
      element: <Search />
    },
    {
      path: "/result",
      element: <Result />
    },
    {
      path: "/load",
      element: <BarLoader />
    }
  ];

  let element = useRoutes(routes);

  return (
    <div>
      {element}
    </div>
  );
}

function Search() {
  return (
    <Container>
      <Starter />
      <hr />
      <SearchBar />
    </Container>
  );
}

function Result() {
  let navigate = useNavigate();
  const { state }: any = useLocation();
  const res = state.result;

  const [show, showElement] = useState(false)
  const [buttonName, setButtonName] = useState('Show Content')

  function showContent() {
    showElement(!show)
  };

  return (
    <div>
      <Container>
        <Starter />
        {
          // Object.keys(res).map(function (key, index) {
          //   const data = res[key];
          //   return (
          //     <div id={data.index}>
          //       <hr />
          //       <div className='jumbotron'>
          //         <p>
          //           <span>Link: </span>
          //           <a href={data.url}><Badge>CLICK HERE</Badge></a>
          //         </p>
          //         <p>{data.text}</p>
          //       </div>
          //     </div>
          //   );
          // })
          res.map((obj: any) => {
            return (
              <div id={obj.index}>
                <hr />
                <div className='jumbotron'>
                  <p>
                    <span>Link: </span>
                    <a href={obj.url}><Badge>CLICK HERE</Badge></a>
                  </p>
                  <p>{obj.headline}</p>
                  <Button
                    onClick={showContent}
                    className='show_content'
                  >
                    {buttonName}
                  </Button>
                  {show ? <div>
                    <br />
                    <p>{obj.content}</p>
                  </div> : null}
                </div>
              </div>
            );
          })
        }
        <br />
      </Container>
      <Button
        variant='success'
        className='full'
        onClick={() => navigate('/')}
      >
        Back
      </Button>
    </div>
  )
}

export default App;
