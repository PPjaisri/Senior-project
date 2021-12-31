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
  let navigate = useNavigate();
  const { state }: any = useLocation();
  const res = state.result;

  return (
    <div>
      <Container>
        <Starter />
        {
          Object.keys(res).map(function (key, index) {
            const data = res[key];
            console.log(data)
            return (
              <div id={data.index}>
                <p>
                  <span>Link: </span>
                  <a href={data.url}>{data.url}</a>
                </p>
                <hr />
                <p>{data.text}</p>
              </div>
            );
          })
        }
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
