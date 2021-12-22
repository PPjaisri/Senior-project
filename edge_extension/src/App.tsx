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

  function onKeyPress(code: string) {
    console.log(code);
    if (code === 'Enter') {
      navigate('/');
    };
  };

  return (
    <div>
      <Container>
        <Starter />
        <p>
          Link: <a href={link} target='_blank'>{link}</a>
        </p>
        <h4>{state.type}</h4>
        <p>{state.data}</p>
      </Container>
      <Button
        variant='success'
        className='full'
        onClick={() => navigate('/')}
        onKeyPress={(event) => onKeyPress(event.code)}
      >
        Back
      </Button>
    </div>
  )
}

export default App;
