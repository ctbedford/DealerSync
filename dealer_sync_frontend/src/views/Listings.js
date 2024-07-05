import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Card from '../components/Card';
import CardContent from '../components/CardContent';
import CardHeader from '../components/CardHeader';
import CardTitle from '../components/CardTitle';
import { Search, Edit, Trash2 } from 'lucide-react';

const Listings = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [listings, setListings] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchListings = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/listings/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        setListings(response.data);
      } catch (err) {
        setError('Failed to fetch listings');
        console.error('Listings fetch error:', err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchListings();
  }, []);

  const handleEdit = async (id) => {
    // Implement edit functionality
    console.log('Edit listing', id);
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:8000/api/listings/${id}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      setListings(listings.filter(listing => listing.id !== id));
    } catch (err) {
      console.error('Delete error:', err);
    }
  };

  const filteredListings = listings.filter(listing =>
    Object.values(listing).some(value =>
      value.toString().toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;

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
              className="flex-grow p-2 border rounded-l-md focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <button className="bg-primary text-white p-2 rounded-r-md hover:bg-primary-dark">
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
          <div className="overflow-x-auto">
            <table className="min-w-full bg-white">
              <thead className="bg-gray-100">
                <tr>
                  <th className="py-2 px-4 text-left">ID</th>
                  <th className="py-2 px-4 text-left">Make</th>
                  <th className="py-2 px-4 text-left">Model</th>
                  <th className="py-2 px-4 text-left">Year</th>
                  <th className="py-2 px-4 text-left">Price</th>
                  <th className="py-2 px-4 text-left">Status</th>
                  <th className="py-2 px-4 text-left">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredListings.map((listing) => (
                  <tr key={listing.id} className="border-b">
                    <td className="py-2 px-4">{listing.id}</td>
                    <td className="py-2 px-4">{listing.make}</td>
                    <td className="py-2 px-4">{listing.model}</td>
                    <td className="py-2 px-4">{listing.year}</td>
                    <td className="py-2 px-4">${listing.price}</td>
                    <td className="py-2 px-4">{listing.status}</td>
                    <td className="py-2 px-4">
                      <button onClick={() => handleEdit(listing.id)} className="text-blue-500 hover:text-blue-700 mr-2">
                        <Edit size={18} />
                      </button>
                      <button onClick={() => handleDelete(listing.id)} className="text-red-500 hover:text-red-700">
                        <Trash2 size={18} />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Listings;
