import { useEffect, useState } from 'react';
import {
  RouteObject,
  useRoutes,
  useNavigate,
  useLocation
} from 'react-router-dom';
import {
  Button,
  Container
} from 'react-bootstrap';
import { Starter, SearchBar, BarLoader } from './Component'
import { getLink } from './Service';

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
      <SearchBar />
    </Container>
  );
}

function Result() {
  let link = 'https://www.example.com/';
  let navigate = useNavigate();
  const { state }: any = useLocation();

  const [type, setType] = useState('');
  const [data, setData] = useState('');

  // async function fetchLink() {
  //   const res = await getLink();

  //   setType(res.message_type);
  //   setData(res.message);
  // };

  // useEffect(() => { 
  //   fetchLink()
  // }, []);

  return (
    <div>
      { console.dir(state) }
      <Container>
        <Starter />
        <p>
          Link: <a href={link} target='_blank'>{link}</a>
        </p>
        {/* <h4>{type}</h4>
        <p>{data}</p> */}
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
