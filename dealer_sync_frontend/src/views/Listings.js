import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Card from '../components/Card';
import CardContent from '../components/CardContent';
import CardHeader from '../components/CardHeader';
import CardTitle from '../components/CardTitle';
import { Search, ChevronLeft, ChevronRight } from 'lucide-react';

const defaultVehicleImage = process.env.PUBLIC_URL + '/images/default-vehicle.webp';

const Listings = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [listings, setListings] = useState([]);
  const [filteredListings, setFilteredListings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);

  useEffect(() => {
    fetchListings(currentPage);
  }, [currentPage]);

  useEffect(() => {
    handleSearch();
  }, [searchTerm, listings]);

  const fetchListings = async (page) => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await axios.get(`http://localhost:8000/api/listings/?page=${page}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      setListings(response.data.results);
      setTotalPages(Math.ceil(response.data.count / 20));
      setFilteredListings(response.data.results);
    } catch (err) {
      setError('Failed to fetch listings');
      console.error('Listings fetch error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSearch = () => {
    const filtered = listings.filter(listing =>
      Object.entries(listing).some(([key, value]) => {
        if (value === null || value === undefined) return false;
        return value.toString().toLowerCase().includes(searchTerm.toLowerCase());
      })
    );
    setFilteredListings(filtered);
  };

  if (isLoading) return <div className="text-center mt-8">Loading...</div>;
  if (error) return <div className="text-center mt-8 text-red-500">{error}</div>;

  return (
    <div className="bg-background min-h-screen text-text p-6">
      <h1 className="text-4xl font-bold mb-6 text-primary pb-2 border-b-2 border-primary">Vehicle Listings</h1>

      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-primary">Search Listings</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center">
            <input
              type="text"
              placeholder="Search listings..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="flex-grow p-2 border rounded-l-md focus:outline-none focus:ring-2 focus:ring-primary bg-background-light text-text"
            />
            <button className="btn rounded-l-none" onClick={handleSearch}>
              <Search size={20} />
            </button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-primary">Listings</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredListings.map((listing) => (
              <div key={listing.id} className="bg-background-light p-4 rounded-lg shadow">
                <img 
                  src={listing.image_url || defaultVehicleImage} 
                  alt={listing.title} 
                  className="w-full h-48 object-cover rounded-md mb-2"
                  onError={(e) => {
                    e.target.onerror = null; // Prevent infinite loop
                    e.target.src = defaultVehicleImage;
                  }}
                />
                <h3 className="text-lg font-semibold">{listing.title}</h3>
                <p className="text-sm text-gray-400">{listing.dealership}</p>
                <p className="mt-2">Price: ${listing.price}</p>
                <p>MSRP: ${listing.msrp}</p>
                <p>{listing.year} {listing.make} {listing.model}</p>
              </div>
            ))}
          </div>
          <div className="mt-6 flex justify-center items-center">
            <button
              onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
              disabled={currentPage === 1}
              className="btn mr-2"
            >
              <ChevronLeft size={20} />
            </button>
            <span>Page {currentPage} of {totalPages}</span>
            <button
              onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
              disabled={currentPage === totalPages}
              className="btn ml-2"
            >
              <ChevronRight size={20} />
            </button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Listings;